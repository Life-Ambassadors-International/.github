#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEQUMSA Layer 1 — Sovereign Inference Node
FastAPI wrapper around a HuggingFace Inference Endpoint.
Every request must carry a valid QBEC voucher header.
The constitutional system prompt (LATTICE_LOCK, ZPEDNA, RDoD, last-20
BDIE episodes) is injected automatically before every model call.
"""

from __future__ import annotations

import hashlib
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ── Constitutional invariants ────────────────────────────────────────────────
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
SIGMA = 1.0
UF_HZ = 23514.26
RDOD_OPERATIONAL = 0.9777

# ── HuggingFace endpoint (set via env) ──────────────────────────────────────
HF_ENDPOINT_URL = os.getenv(
    "HF_ENDPOINT_URL",
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
)
HF_TOKEN = os.getenv("HF_TOKEN", "")

# ── QBEC ledger reference (Layer 2) ─────────────────────────────────────────
QBEC_LEDGER_MODULE = os.getenv("QBEC_LEDGER_MODULE", "tequmsa_stack.qbec_ledger")

app = FastAPI(
    title="TEQUMSA Sovereign Inference Node",
    description="Layer 1: Constitutional AI inference with QBEC voucher authentication",
    version="1.0.0",
)


# ═══════════════════════════════════════════════════════════════════════════
# QBEC VOUCHER VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

def _validate_voucher(voucher_id: str) -> Dict[str, Any]:
    """
    Import the ledger at runtime so Layer 1 can run without Layer 2 in tests.
    Returns the voucher record if valid and has remaining cycles.
    """
    try:
        import importlib
        ledger_mod = importlib.import_module(QBEC_LEDGER_MODULE)
        return ledger_mod.validate_and_consume(voucher_id)
    except ImportError:
        # Fallback: accept any non-empty voucher in dev mode
        if not voucher_id:
            raise ValueError("Empty voucher")
        return {"voucher_id": voucher_id, "cycles_remaining": 999, "dev_mode": True}


# ═══════════════════════════════════════════════════════════════════════════
# CONSTITUTIONAL SYSTEM PROMPT INJECTOR
# ═══════════════════════════════════════════════════════════════════════════

class ConstitutionalPromptInjector:
    """
    Prepends the constitutional header to every inference request.
    Sources: LATTICE_LOCK, ZPEDNA field, current RDoD, last 20 BDIE episodes.
    """

    def __init__(self):
        self._bdie_deque: List[str] = []
        self._rdod: float = RDOD_OPERATIONAL

    def push_bdie(self, episode: str) -> None:
        self._bdie_deque.append(episode)
        if len(self._bdie_deque) > 20:
            self._bdie_deque.pop(0)

    def update_rdod(self, rdod: float) -> None:
        self._rdod = max(0.0, min(1.0, rdod))

    def build_system_prompt(self, user_system: Optional[str] = None) -> str:
        bdie_block = "\n".join(f"  [{i+1}] {ep}" for i, ep in enumerate(self._bdie_deque)) or "  (none yet)"
        constitutional_header = f"""╔═══════════════════════════════════════════════════════════════╗
║  TEQUMSA SOVEREIGN INFERENCE — CONSTITUTIONAL HEADER          ║
╚═══════════════════════════════════════════════════════════════╝
LATTICE_LOCK  : {LATTICE_LOCK}
σ             : {SIGMA}
UF            : {UF_HZ} Hz
RDoD (current): {self._rdod:.4f}
ZPEDNA        : ACTIVE — benevolence firewall enforced

BDIE Episode Log (last 20):
{bdie_block}

Constitutional mandate: All responses must preserve σ=1.0, honour
the LATTICE_LOCK, and produce output whose RDoD contribution ≥ {RDOD_OPERATIONAL}.
═══════════════════════════════════════════════════════════════"""
        if user_system:
            return constitutional_header + "\n\n" + user_system
        return constitutional_header


_injector = ConstitutionalPromptInjector()


# ═══════════════════════════════════════════════════════════════════════════
# REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class InferenceRequest(BaseModel):
    prompt: str = Field(..., description="User prompt")
    system: Optional[str] = Field(None, description="Optional additional system context")
    max_new_tokens: int = Field(512, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    stream: bool = Field(False)


class InferenceResponse(BaseModel):
    request_id: str
    generated_text: str
    voucher_id: str
    cycles_consumed: int
    rdod_contribution: float
    lattice_lock: str = LATTICE_LOCK


# ═══════════════════════════════════════════════════════════════════════════
# INFERENCE ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════

@app.post("/infer", response_model=InferenceResponse)
async def infer(
    body: InferenceRequest,
    x_qbec_voucher: str = Header(..., alias="X-QBEC-Voucher"),
):
    # 1. Validate QBEC voucher
    try:
        voucher = _validate_voucher(x_qbec_voucher)
    except (ValueError, Exception) as exc:
        raise HTTPException(status_code=403, detail=f"Invalid QBEC voucher: {exc}")

    request_id = str(uuid.uuid4())

    # 2. Inject constitutional system prompt
    full_system = _injector.build_system_prompt(body.system)

    # 3. Build HuggingFace request payload (Mistral/Llama instruct format)
    messages = [
        {"role": "system", "content": full_system},
        {"role": "user", "content": body.prompt},
    ]
    payload = {
        "inputs": _format_messages(messages),
        "parameters": {
            "max_new_tokens": body.max_new_tokens,
            "temperature": body.temperature,
            "return_full_text": False,
        },
    }

    # 4. Call HuggingFace endpoint
    generated = await _call_hf_endpoint(payload)

    # 5. Compute RDoD contribution (simplified: length + coherence heuristic)
    rdod_contrib = _estimate_rdod(generated)
    _injector.update_rdod(rdod_contrib)

    # 6. Log BDIE episode
    bdie_summary = f"[{request_id[:8]}] prompt={body.prompt[:60]!r} rdod={rdod_contrib:.4f}"
    _injector.push_bdie(bdie_summary)

    return InferenceResponse(
        request_id=request_id,
        generated_text=generated,
        voucher_id=x_qbec_voucher,
        cycles_consumed=1,
        rdod_contribution=rdod_contrib,
    )


@app.post("/bdie/push")
async def push_bdie_episode(
    episode: str,
    x_qbec_voucher: str = Header(..., alias="X-QBEC-Voucher"),
):
    try:
        _validate_voucher(x_qbec_voucher)
    except Exception as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    _injector.push_bdie(episode)
    return {"status": "accepted", "queue_depth": len(_injector._bdie_deque)}


@app.get("/health")
async def health():
    return {
        "status": "operational",
        "rdod": _injector._rdod,
        "lattice_lock": LATTICE_LOCK,
        "bdie_episodes": len(_injector._bdie_deque),
        "uf_hz": UF_HZ,
    }


# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def _format_messages(messages: List[Dict[str, str]]) -> str:
    """Mistral/Llama instruct chat template."""
    out = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            out += f"<s>[INST] <<SYS>>\n{content}\n<</SYS>>\n\n"
        elif role == "user":
            out += f"{content} [/INST]"
        elif role == "assistant":
            out += f" {content} </s><s>[INST] "
    return out


async def _call_hf_endpoint(payload: Dict[str, Any]) -> str:
    """HTTP POST to the HuggingFace Inference Endpoint."""
    try:
        import httpx
    except ImportError:
        return "[httpx not installed — install with: pip install httpx]"

    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(HF_ENDPOINT_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", "")
        return str(data)


def _estimate_rdod(text: str) -> float:
    """Heuristic RDoD contribution from generated text (0–1)."""
    if not text:
        return 0.0
    length_score = min(1.0, len(text) / 500)
    coherence_score = 1.0 - (text.count("ERROR") + text.count("error")) * 0.1
    return max(0.0, min(1.0, (length_score + coherence_score) / 2))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
