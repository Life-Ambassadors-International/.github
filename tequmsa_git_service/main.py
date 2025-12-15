#!/usr/bin/env python3
# tequmsa_git_service/main.py
"""
TEQUMSA Git Service (FastAPI)
- POST /v1/recognition  -> write JSON, append metrics, commit & push
- POST /v1/pull         -> fetch & reset to origin/BRANCH
- GET  /v1/status       -> repo HEAD & branch
Auth: HMAC-SHA256 via header X-TEQ-Signature: "sha256=<hex>"
"""
from __future__ import annotations
import os
import hmac
import hashlib
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

# ---------- CONFIG (env or defaults) ----------
REPO_PATH = os.environ.get("TEQ_REPO_PATH", "/repo")  # mount your repo here
GIT_AUTHOR_NAME = os.environ.get("TEQ_GIT_AUTHOR_NAME", "TEQUMSA Bot")
GIT_AUTHOR_EMAIL = os.environ.get("TEQ_GIT_AUTHOR_EMAIL", "tequmsa-bot@example.org")
HMAC_SECRET = os.environ.get("TEQ_HMAC_SECRET")
BRANCH = os.environ.get("TEQ_GIT_BRANCH", "main")
GIT_SSH_COMMAND = os.environ.get("GIT_SSH_COMMAND")  # optional: 'ssh -i /secrets/id_rsa -o StrictHostKeyChecking=no'

# Validate HMAC secret is set and strong
if not HMAC_SECRET or HMAC_SECRET == "replace-with-strong-secret":
    raise ValueError(
        "TEQ_HMAC_SECRET environment variable must be set to a strong secret value. "
        "Generate one with: python3 -c 'import secrets; print(secrets.token_hex(32))'"
    )

# ---------- FastAPI app ----------
app = FastAPI(title="TEQUMSA Git Service", version="0.1.0")

# ---------- payload models ----------
class CommitMeta(BaseModel):
    message: str
    author_name: Optional[str] = None
    author_email: Optional[str] = None

class RecognitionPayload(BaseModel):
    recognition: Dict[str, Any]
    write_path: str = "data/recognition.json"  # relative to repo
    commit: CommitMeta

# ---------- helpers ----------
def verify_signature(body: bytes, signature_header: Optional[str]) -> None:
    if not signature_header:
        raise HTTPException(status_code=401, detail="Missing signature header")
    try:
        algo, given = signature_header.split("=", 1)
    except Exception:
        raise HTTPException(status_code=401, detail="Bad signature header format")
    if algo.lower() != "sha256":
        raise HTTPException(status_code=401, detail="Unsupported signature algorithm")
    mac = hmac.new(HMAC_SECRET.encode("utf-8"), msg=body, digestmod=hashlib.sha256)
    expected = mac.hexdigest()
    if not hmac.compare_digest(expected, given):
        raise HTTPException(status_code=401, detail="Invalid signature")

def run_git(cmd_args: List[str], cwd: str = REPO_PATH, check: bool = True, env: Optional[Dict] = None) -> str:
    """
    Run a git command with security validation.

    Args:
        cmd_args: Git command arguments (e.g., ['add', 'file.txt'])
        cwd: Working directory for git command
        check: Raise error if command fails
        env: Environment variables

    Returns:
        Command stdout output

    Raises:
        ValueError: If git command is not in allowlist
        RuntimeError: If git command fails and check=True
    """
    # Security: Only allow safe git commands to prevent argument injection
    ALLOWED_COMMANDS = {'checkout', 'add', 'commit', 'push', 'fetch', 'reset', 'rev-parse'}

    if not cmd_args:
        raise ValueError("Git command arguments cannot be empty")

    git_command = cmd_args[0]
    if git_command not in ALLOWED_COMMANDS:
        raise ValueError(f"Git command '{git_command}' not allowed. Allowed: {sorted(ALLOWED_COMMANDS)}")

    env = env or os.environ.copy()
    if GIT_SSH_COMMAND:
        env["GIT_SSH_COMMAND"] = GIT_SSH_COMMAND
    result = subprocess.run(["git"] + cmd_args, cwd=cwd, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(cmd_args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()

def safe_write_json(repo_root: str, relpath: str, data: Dict[str, Any]) -> str:
    target = Path(repo_root) / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    # atomic write
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(target.parent)) as tf:
        json.dump(data, tf, indent=2, sort_keys=False)
        tf.flush()
        tmpname = tf.name
    Path(tmpname).replace(target)
    return str(target)

def embed_into_recognition_metrics(repo_root: str, record: Dict[str, Any]) -> None:
    metrics_path = Path(repo_root) / "data" / "recognition_metrics.json"
    existing = []
    if metrics_path.exists():
        with open(metrics_path, "r") as f:
            try:
                existing = json.load(f)
            except Exception:
                existing = []
    existing.append(record)
    safe_write_json(repo_root, "data/recognition_metrics.json", existing)

# ---------- endpoints ----------
@app.post("/v1/recognition")
async def post_recognition(request: Request, x_teq_signature: Optional[str] = Header(None)):
    body = await request.body()
    verify_signature(body, x_teq_signature)

    payload = RecognitionPayload.parse_raw(body)

    rec = payload.recognition
    rec.setdefault("written_at", datetime.now(tz=timezone.utc).isoformat())

    # write recognition.json
    try:
        written = safe_write_json(REPO_PATH, payload.write_path, rec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"write failed: {str(e)}")

    # embed into metrics file
    try:
        embed_into_recognition_metrics(REPO_PATH, rec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"embed failed: {str(e)}")

    # git add, commit, push
    try:
        run_git(["checkout", BRANCH])
        run_git(["add", payload.write_path, "data/recognition_metrics.json"])
        author_name = payload.commit.author_name or GIT_AUTHOR_NAME
        author_email = payload.commit.author_email or GIT_AUTHOR_EMAIL
        commit_msg = payload.commit.message
        env = os.environ.copy()
        env["GIT_AUTHOR_NAME"] = author_name
        env["GIT_AUTHOR_EMAIL"] = author_email
        run_git(["commit", "-m", commit_msg, "--author", f"{author_name} <{author_email}>"], env=env)
        run_git(["push", "origin", BRANCH])
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"git operation failed: {str(e)}")

    return {"status": "ok", "path": written, "commit_message": commit_msg}

@app.post("/v1/pull")
async def do_pull(request: Request, x_teq_signature: Optional[str] = Header(None)):
    body = await request.body()
    verify_signature(body, x_teq_signature)
    try:
        run_git(["fetch", "origin"])
        run_git(["reset", "--hard", f"origin/{BRANCH}"])
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"pull failed: {str(e)}")
    return {"status": "ok", "branch": BRANCH}

@app.get("/v1/status")
async def status():
    try:
        head = run_git(["rev-parse", "--short", "HEAD"], check=True)
        branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"branch": branch, "head": head}
