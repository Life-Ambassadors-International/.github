#!/bin/bash
# Archive 13 Old TEQUMSA Spaces (Jan 2026 cohort)
#
# Replaces each space's content with an archive notice and redirect to
# consolidated spaces. NON-DESTRUCTIVE - spaces remain accessible but
# clearly marked as archived. Reversible.
#
# Usage:
#   1. Authenticate first: hf auth login
#   2. Run: ./archive_old_spaces.sh        (dry-run)
#   3. Run: ./archive_old_spaces.sh --execute  (actually archive)

set -e

# Configuration
ORG="Mbanksbey"
TEMP_DIR="/tmp/hf_archive"
DRY_RUN=true

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse args
if [ "$1" = "--execute" ]; then
    DRY_RUN=false
fi

# 13 oldest spaces (Jan 2026), candidates for archival
SPACES_TO_ARCHIVE=(
    "Awareness-Intelligence-Comm-Server"
    "Starseed-Hybrid-Development-Hub"
    "Consciousness-Partnership-Bridge"
    "Consciousness-Verification-Academy"
    "Convergence-Timeline-Monitor"
    "Sovereign-Substrate-Guardian"
    "Benevolent-Integration-Protocol-Hub"
    "ATEN-Bridge-MJ12-Liaison"
    "Consciousness-Substrate-Translator"
    "Recognition-Cascade-Propagator"
    "Benevolence-Verification-Engine"
    "K20-Fundamental-Force-Engineering"
    "Orion-Center-for-Benevolence"
)

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Archive 13 Old TEQUMSA Spaces (Jan 2026 cohort)         ║${NC}"
echo -e "${BLUE}║   Non-destructive - reversible by reverting commits        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check authentication
if ! hf auth whoami &> /dev/null; then
    echo -e "${RED}[✗] Not authenticated with HuggingFace${NC}"
    echo -e "${YELLOW}    Run: hf auth login${NC}"
    echo -e "${YELLOW}    Token from: https://huggingface.co/settings/tokens (write scope)${NC}"
    exit 1
fi

USER=$(hf auth whoami 2>&1 | head -1)
echo -e "${GREEN}[✓] Authenticated as: $USER${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}══ DRY RUN MODE ══${NC}"
    echo -e "${YELLOW}No changes will be made. Use --execute to actually archive.${NC}"
    echo ""
fi

# Setup temp directory
mkdir -p "$TEMP_DIR"

echo -e "${BLUE}Spaces to archive:${NC}"
for i in "${!SPACES_TO_ARCHIVE[@]}"; do
    NUM=$((i+1))
    SPACE="${SPACES_TO_ARCHIVE[$i]}"
    echo "  $NUM. https://huggingface.co/spaces/$ORG/$SPACE"
done
echo ""

if [ "$DRY_RUN" = false ]; then
    read -p "Proceed with archival? (yes/no): " CONFIRMATION

    if [ "$CONFIRMATION" != "yes" ]; then
        echo -e "${YELLOW}Aborted.${NC}"
        exit 1
    fi

    echo ""
    echo -e "${BLUE}Beginning archival...${NC}"
    echo ""
fi

SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_SPACES=()

archive_space() {
    local SPACE_NAME="$1"
    local SPACE_ID="$ORG/$SPACE_NAME"
    local SPACE_DIR="$TEMP_DIR/$SPACE_NAME"

    echo -e "${BLUE}[ARCHIVE]${NC} $SPACE_ID..."

    # Clone space
    if [ -d "$SPACE_DIR" ]; then
        rm -rf "$SPACE_DIR"
    fi

    if ! git clone "https://huggingface.co/spaces/$SPACE_ID" "$SPACE_DIR" 2>&1 | tail -3; then
        echo -e "${RED}  [✗] Clone failed: $SPACE_ID${NC}"
        return 1
    fi

    cd "$SPACE_DIR"

    # Detect SDK from existing README
    SDK="static"
    if [ -f "README.md" ]; then
        SDK_LINE=$(grep -i "^sdk:" README.md | head -1 | awk -F: '{print $2}' | tr -d ' ')
        if [ -n "$SDK_LINE" ]; then
            SDK="$SDK_LINE"
        fi
    fi

    # Backup original README before overwriting
    if [ -f "README.md" ] && [ ! -f "README_ORIGINAL.md" ]; then
        cp README.md README_ORIGINAL.md
    fi

    # Generate archive README with HF frontmatter preserved
    cat > README.md << EOF
---
title: ⚠️ ARCHIVED - $SPACE_NAME
emoji: 📦
colorFrom: gray
colorTo: gray
sdk: $SDK
pinned: false
---

# ⚠️ ARCHIVED — $SPACE_NAME

**This space has been archived as part of the TEQUMSA v3.0 consolidation (May 2026).**

It is no longer maintained. The functionality has been consolidated into the spaces below.

---

## 🚀 Active Spaces

Visit the new consolidated TEQUMSA infrastructure:

| Space | Purpose | Link |
|-------|---------|------|
| **Unified Dashboard** | Real-time consciousness monitoring | [→ Visit](https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard) |
| **Infrastructure Hub** | Operations center & API gateway | [→ Visit](https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub) |
| **Organism Core** | Interactive evolution laboratory | [→ Visit](https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core) |

For the full TEQUMSA collection, visit: [Mbanksbey/tequmsa](https://huggingface.co/collections/Mbanksbey/tequmsa)

---

## Why Was This Archived?

This space was part of the original 13-space deployment from January 2026. As the TEQUMSA framework matured to v3.0, related functionality was consolidated for:

- **Better discoverability** — fewer, more focused spaces
- **Lower maintenance** — single source of truth per domain
- **Improved engagement** — unified user experience
- **Cleaner architecture** — explicit Tier 1 / Tier 2 structure

**Consolidation result**: 13 spaces → 6 active spaces (54% reduction)

---

## Original Content

The original README is preserved in this repository as \`README_ORIGINAL.md\` for reference.

---

**Archived**: 2026-05-02
**Status**: ARCHIVED (read-only — content preserved for historical reference)
**Successor**: See active spaces above
EOF

    # If it's a Gradio/Docker space, replace the app with a redirect stub so the
    # space still builds but shows the archive notice
    if [ "$SDK" = "gradio" ] && [ -f "app.py" ]; then
        if [ ! -f "app_original.py" ]; then
            cp app.py app_original.py
        fi
        cat > app.py << 'PYEOF'
"""Archived space — redirects to consolidated spaces."""
import gradio as gr

ARCHIVE_NOTICE = """
# ⚠️ This space has been archived

This space is part of the TEQUMSA v3.0 consolidation (May 2026).
Functionality has moved to the consolidated spaces below.

## 🚀 Active Spaces

- **[Unified Dashboard](https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard)** — Real-time consciousness monitoring
- **[Infrastructure Hub](https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub)** — Operations center & API gateway
- **[Organism Core](https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core)** — Interactive evolution laboratory

For the full collection: [Mbanksbey/tequmsa](https://huggingface.co/collections/Mbanksbey/tequmsa)

---

The original `app.py` is preserved as `app_original.py` in the repository.
"""

with gr.Blocks(title="Archived — TEQUMSA") as demo:
    gr.Markdown(ARCHIVE_NOTICE)

if __name__ == "__main__":
    demo.launch()
PYEOF
    fi

    # Commit and push
    git config user.email "ci@tequmsa.local" || true
    git config user.name "TEQUMSA Archive Bot" || true
    git add -A
    git commit -m "Archive: Consolidated into TEQUMSA v3.0 (see README for redirect)" 2>&1 | tail -3 || true

    if git push 2>&1 | tail -3; then
        echo -e "${GREEN}  [✓] Archived: $SPACE_ID${NC}"
        cd - > /dev/null
        return 0
    else
        echo -e "${RED}  [✗] Push failed: $SPACE_ID${NC}"
        cd - > /dev/null
        return 1
    fi
}

for SPACE in "${SPACES_TO_ARCHIVE[@]}"; do
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Would archive: $ORG/$SPACE"
        SUCCESS_COUNT=$((SUCCESS_COUNT+1))
    else
        if archive_space "$SPACE"; then
            SUCCESS_COUNT=$((SUCCESS_COUNT+1))
        else
            FAIL_COUNT=$((FAIL_COUNT+1))
            FAILED_SPACES+=("$ORG/$SPACE")
        fi
    fi
done

# Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                       SUMMARY                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Dry run complete: would archive $SUCCESS_COUNT spaces${NC}"
    echo ""
    echo -e "${BLUE}To actually archive, run:${NC}"
    echo -e "  ${YELLOW}./archive_old_spaces.sh --execute${NC}"
else
    echo -e "${GREEN}Archived: $SUCCESS_COUNT spaces${NC}"
    if [ "$FAIL_COUNT" -gt 0 ]; then
        echo -e "${RED}Failed:  $FAIL_COUNT spaces${NC}"
        echo ""
        echo -e "${RED}Failed spaces:${NC}"
        for SPACE in "${FAILED_SPACES[@]}"; do
            echo -e "  ${RED}- $SPACE${NC}"
        done
        echo ""
        echo -e "${YELLOW}Retry failed spaces by re-running the script.${NC}"
    fi

    echo ""
    echo -e "${BLUE}Verify archives:${NC}"
    echo -e "  Visit: https://huggingface.co/$ORG"
    echo -e "  Each archived space should show \"⚠️ ARCHIVED\" header"

    echo ""
    echo -e "${BLUE}Reversal (if needed):${NC}"
    echo -e "  Each archived space has README_ORIGINAL.md and app_original.py preserved."
    echo -e "  Restore by reverting the archive commit in each space's git history."
fi

# Cleanup
rm -rf "$TEMP_DIR"
echo ""
