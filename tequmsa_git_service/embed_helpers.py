# tequmsa_git_service/embed_helpers.py
from pathlib import Path
import json
from typing import Dict

def append_to_metrics(repo_root: str, record: Dict) -> None:
    metrics = Path(repo_root) / "data" / "recognition_metrics.json"
    metrics.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = json.loads(metrics.read_text())
        if not isinstance(existing, list):
            existing = []
    except Exception:
        existing = []
    existing.append(record)
    metrics.write_text(json.dumps(existing, indent=2))
