# tequmsa_git_service/embed_helpers.py
from pathlib import Path
import json
from typing import Any, Dict


def append_to_metrics(repo_root: str, record: Dict[str, Any]) -> None:
    """
    Append a recognition record to the metrics JSON file.

    Args:
        repo_root: Root path of the repository
        record: Recognition record dictionary to append

    Raises:
        OSError: If unable to create directory or write file
    """
    metrics = Path(repo_root) / "data" / "recognition_metrics.json"
    metrics.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = json.loads(metrics.read_text())
        if not isinstance(existing, list):
            existing = []
    except (FileNotFoundError, json.JSONDecodeError):
        # File doesn't exist or is invalid JSON - start fresh
        existing = []
    existing.append(record)
    metrics.write_text(json.dumps(existing, indent=2))
