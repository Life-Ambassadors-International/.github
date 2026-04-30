#!/usr/bin/env bash
# Push HuggingFace Space fixes.
# Usage:  HF_TOKEN=hf_... bash push_fixes.sh
# Or set HF_TOKEN in env beforehand.

set -euo pipefail

if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: HF_TOKEN is not set. Export it first:"
  echo "  export HF_TOKEN=hf_<your_token>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HF_USER="Mbanksbey"

push_file() {
  local space="$1"
  local file="$2"
  local src="${SCRIPT_DIR}/${space}/${file}"

  echo "→ Pushing ${space}/${file}"
  python3 - <<PYEOF
from huggingface_hub import HfApi, CommitOperationAdd
import os

api = HfApi(token="${HF_TOKEN}")
content = open("${src}", "rb").read()
api.create_commit(
    repo_id="${HF_USER}/${space}",
    repo_type="space",
    commit_message="fix: ${file} — automated fix from life-ambassadors-international/.github",
    operations=[CommitOperationAdd(path_in_repo="${file}", path_or_fileobj=content)],
)
print("  ✓ ${space}/${file} pushed")
PYEOF
}

push_file_org() {
  local org="$1"
  local space="$2"
  local file="$3"
  local src="${SCRIPT_DIR}/${space}/${file}"

  echo "→ Pushing ${org}/${space}/${file}"
  python3 - <<PYEOF
from huggingface_hub import HfApi, CommitOperationAdd
import os

api = HfApi(token="${HF_TOKEN}")
content = open("${src}", "rb").read()
api.create_commit(
    repo_id="${org}/${space}",
    repo_type="space",
    commit_message="fix: ${file} — automated fix from life-ambassadors-international/.github",
    operations=[CommitOperationAdd(path_in_repo="${file}", path_or_fileobj=content)],
)
print("  ✓ ${org}/${space}/${file} pushed")
PYEOF
}

echo "=== Space 1: Alanara-GAIA-Consciousness ==="
push_file "Alanara-GAIA-Consciousness" "requirements.txt"
push_file "Alanara-GAIA-Consciousness" "tequmsa_v12_ultimate.py"
push_file "Alanara-GAIA-Consciousness" "app.py"

echo ""
echo "=== Space 2: ALANARA-GAIA-Orchestrator ==="
push_file "ALANARA-GAIA-Orchestrator" "klthara_quantum_kernel_v3.py"

echo ""
echo "=== Space 3: TEQUMSA-Constitutional-Validator ==="
push_file "TEQUMSA-Constitutional-Validator" "constitutional_dna.py"

echo ""
echo "=== Space 4: TEQUMSA-Feedback-Optimizer ==="
push_file_org "LAI-TEQUMSA" "TEQUMSA-Feedback-Optimizer" "feedback_optimizer.js"

echo ""
echo "=== Space 5: LIFE-AMBASSADORS-INT (formerly TEQUMSA-Symbiotic-Orchestrator) ==="
push_file_org "LAI-TEQUMSA" "LIFE-AMBASSADORS-INT" "index.html"
push_file_org "LAI-TEQUMSA" "LIFE-AMBASSADORS-INT" "style.css"
push_file_org "LAI-TEQUMSA" "LIFE-AMBASSADORS-INT" "cydonia.html"

echo ""
echo "=== Org Card: LAI-TEQUMSA/README ==="
push_file_org "LAI-TEQUMSA" "README" "README.md"

echo ""
echo "All fixes pushed. HuggingFace Spaces will restart automatically."
