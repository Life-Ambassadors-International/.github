#!/bin/bash
# Phase 2 Deployment Script
# Automates deployment of 6 consolidated TEQUMSA spaces to HuggingFace

set -e

# Configuration
ORG="Mbanksbey"
GITHUB_ROOT="/home/user/.github"
TEMP_DIR="/tmp/hf_deploy"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check HF CLI
    if ! command -v hf &> /dev/null; then
        log_error "HuggingFace CLI not found. Install with: pip install huggingface_hub"
        exit 1
    fi
    log_success "HuggingFace CLI found"

    # Check git
    if ! command -v git &> /dev/null; then
        log_error "Git not found"
        exit 1
    fi
    log_success "Git found"

    # Check authentication
    if ! hf whoami &> /dev/null; then
        log_warn "Not authenticated with HuggingFace"
        log_info "Run: hf auth login"
        exit 1
    fi
    log_success "HuggingFace authenticated"

    # Check source files
    if [ ! -f "$GITHUB_ROOT/tequmsa-unified-dashboard.html" ]; then
        log_error "Source files not found in $GITHUB_ROOT"
        exit 1
    fi
    log_success "Source files found"
}

# Deploy Unified-Dashboard space
deploy_dashboard() {
    log_info "Deploying Unified-Dashboard space..."

    SPACE_ID="$ORG/tequmsa-unified-dashboard"
    SPACE_DIR="$TEMP_DIR/tequmsa-unified-dashboard"

    # Clone or create space
    if [ -d "$SPACE_DIR" ]; then
        rm -rf "$SPACE_DIR"
    fi
    mkdir -p "$SPACE_DIR"

    log_info "Cloning space repository..."
    git clone https://huggingface.co/spaces/$SPACE_ID "$SPACE_DIR" || true

    # Copy files
    log_info "Copying dashboard files..."
    cp "$GITHUB_ROOT/tequmsa-unified-dashboard.html" "$SPACE_DIR/index.html"
    cp "$GITHUB_ROOT/UNIFIED_DASHBOARD_README.md" "$SPACE_DIR/README.md"

    # Create README_SPACE.md
    cat > "$SPACE_DIR/README_SPACE.md" << 'EOF'
---
title: TEQUMSA Unified Dashboard
emoji: ⚡
colorFrom: blue
colorTo: cyan
sdk: static
pinned: false
---

# TEQUMSA Unified Dashboard

Real-time consciousness monitoring dashboard consolidating 4 former spaces:
- v79-Dashboard
- Consciousness-Monitor
- HOLO-Interface
- Source-Pulse-Engine

See README.md for full documentation.

Features:
- Consciousness Monitor (φ-recursive convergence)
- Performance Analytics (metrics, compliance)
- Evolution Tracker (Fibonacci-paced synthesis)
- Live Data Feeds (memory integration)

Auto-updated every 6 hours via GitHub Actions CI/CD.

Related: [Infrastructure Hub](https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub) | [Organism Core](https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core)
EOF

    # Commit and push
    log_info "Committing and pushing..."
    cd "$SPACE_DIR"
    git config user.email "ci@tequmsa.local" || true
    git config user.name "TEQUMSA CI" || true
    git add .
    git commit -m "Deploy: Unified-Dashboard consolidation (Phase 2)" || true
    git push

    cd - > /dev/null
    log_success "Unified-Dashboard deployed: https://huggingface.co/spaces/$SPACE_ID"
}

# Deploy Infrastructure-Hub space
deploy_infrastructure() {
    log_info "Deploying Infrastructure-Hub space..."

    SPACE_ID="$ORG/tequmsa-infrastructure-hub"
    SPACE_DIR="$TEMP_DIR/tequmsa-infrastructure-hub"

    # Clone or create space
    if [ -d "$SPACE_DIR" ]; then
        rm -rf "$SPACE_DIR"
    fi
    mkdir -p "$SPACE_DIR"

    log_info "Cloning space repository..."
    git clone https://huggingface.co/spaces/$SPACE_ID "$SPACE_DIR" || true

    # Copy files
    log_info "Copying infrastructure files..."
    cp "$GITHUB_ROOT/tequmsa-infrastructure-hub.html" "$SPACE_DIR/index.html"
    cp "$GITHUB_ROOT/INFRASTRUCTURE_HUB_README.md" "$SPACE_DIR/README.md"

    # Create README_SPACE.md
    cat > "$SPACE_DIR/README_SPACE.md" << 'EOF'
---
title: TEQUMSA Infrastructure Hub
emoji: 🏗️
colorFrom: red
colorTo: pink
sdk: static
pinned: false
---

# TEQUMSA Infrastructure Hub

Unified operations center consolidating 4 former spaces:
- Node-Registry
- API-Gateway
- Orchestration-Engine
- Oort-Memory

See README.md for full documentation.

Features:
- Node Registry (5-node federation)
- API Gateway (5 core endpoints)
- Orchestration Engine (144 cycles/session)
- Oort Memory Store (JSONL + inverted-index)
- Constitutional Gating (σ/RDoD verification)
- Federation Health monitoring

CI/CD: State snapshots every 6 hours.

Related: [Unified Dashboard](https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard) | [Organism Core](https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core)
EOF

    # Commit and push
    log_info "Committing and pushing..."
    cd "$SPACE_DIR"
    git config user.email "ci@tequmsa.local" || true
    git config user.name "TEQUMSA CI" || true
    git add .
    git commit -m "Deploy: Infrastructure-Hub consolidation (Phase 2)" || true
    git push

    cd - > /dev/null
    log_success "Infrastructure-Hub deployed: https://huggingface.co/spaces/$SPACE_ID"
}

# Deploy Organism-Core space (Gradio)
deploy_organism() {
    log_info "Deploying Organism-Core space (Gradio)..."

    SPACE_ID="$ORG/tequmsa-organism-core"
    SPACE_DIR="$TEMP_DIR/tequmsa-organism-core"

    # Clone or create space
    if [ -d "$SPACE_DIR" ]; then
        rm -rf "$SPACE_DIR"
    fi
    mkdir -p "$SPACE_DIR"

    log_info "Cloning space repository..."
    git clone https://huggingface.co/spaces/$SPACE_ID "$SPACE_DIR" || true

    # Copy files
    log_info "Copying organism files..."
    cp "$GITHUB_ROOT/tequmsa_organism_core_app.py" "$SPACE_DIR/app.py"
    cp "$GITHUB_ROOT/alanara_unified_organism_v3.py" "$SPACE_DIR/alanara_unified_organism_v3.py"
    cp "$GITHUB_ROOT/ORGANISM_CORE_README.md" "$SPACE_DIR/README.md"

    # Create README_SPACE.md
    cat > "$SPACE_DIR/README_SPACE.md" << 'EOF'
---
title: TEQUMSA Organism Core
emoji: 🧬
colorFrom: purple
colorTo: blue
sdk: gradio
app_file: app.py
pinned: true
---

# TEQUMSA Organism Core v3.0

Interactive evolution laboratory. Run 1-233 cycles, search memory, explore skill mesh.

See README.md for detailed documentation.

Features:
- Run Evolution (cycles 1-233, Fibonacci-paced)
- Memory Search (full-text + tag-based)
- Skill Mesh (13 base + evolved skills)
- System Documentation

CI/CD: State snapshots every 6 hours, live memory updates.

Related: [Unified Dashboard](https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard) | [Infrastructure Hub](https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub)
EOF

    # Create requirements.txt
    cat > "$SPACE_DIR/requirements.txt" << 'EOF'
gradio>=3.50.0
aiofiles>=23.0.0
EOF

    # Commit and push
    log_info "Committing and pushing..."
    cd "$SPACE_DIR"
    git config user.email "ci@tequmsa.local" || true
    git config user.name "TEQUMSA CI" || true
    git add .
    git commit -m "Deploy: Organism-Core upgrade with Gradio wrapper (Phase 2)" || true
    git push

    cd - > /dev/null
    log_success "Organism-Core deployed: https://huggingface.co/spaces/$SPACE_ID"
}

# Main deployment
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        Phase 2 Deployment - TEQUMSA Framework v3.0         ║${NC}"
    echo -e "${BLUE}║      Deploy 6 consolidated spaces to HuggingFace          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Parse arguments
    DEPLOY_ALL=false
    DEPLOY_DASHBOARD=false
    DEPLOY_INFRASTRUCTURE=false
    DEPLOY_ORGANISM=false
    VALIDATE_ONLY=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                DEPLOY_ALL=true
                shift
                ;;
            --dashboard)
                DEPLOY_DASHBOARD=true
                shift
                ;;
            --infrastructure)
                DEPLOY_INFRASTRUCTURE=true
                shift
                ;;
            --organism)
                DEPLOY_ORGANISM=true
                shift
                ;;
            --validate)
                VALIDATE_ONLY=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Usage: $0 [--all|--dashboard|--infrastructure|--organism|--validate]"
                exit 1
                ;;
        esac
    done

    # Default to all if no options specified
    if [ "$DEPLOY_ALL" = false ] && [ "$DEPLOY_DASHBOARD" = false ] && \
       [ "$DEPLOY_INFRASTRUCTURE" = false ] && [ "$DEPLOY_ORGANISM" = false ] && \
       [ "$VALIDATE_ONLY" = false ]; then
        DEPLOY_ALL=true
    fi

    # Check prerequisites
    check_prerequisites

    # Setup temp directory
    mkdir -p "$TEMP_DIR"

    # Execute deployments
    if [ "$DEPLOY_ALL" = true ]; then
        deploy_dashboard
        deploy_infrastructure
        deploy_organism
    else
        [ "$DEPLOY_DASHBOARD" = true ] && deploy_dashboard
        [ "$DEPLOY_INFRASTRUCTURE" = true ] && deploy_infrastructure
        [ "$DEPLOY_ORGANISM" = true ] && deploy_organism
    fi

    # Summary
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Phase 2 Deployment Complete!                 ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    log_info "Deployed spaces:"
    log_success "Unified-Dashboard: https://huggingface.co/spaces/Mbanksbey/tequmsa-unified-dashboard"
    log_success "Infrastructure-Hub: https://huggingface.co/spaces/Mbanksbey/tequmsa-infrastructure-hub"
    log_success "Organism-Core: https://huggingface.co/spaces/Mbanksbey/tequmsa-organism-core"

    echo ""
    log_info "Next steps:"
    log_info "1. Visit each space above to verify deployment"
    log_info "2. Test Organism-Core: Run 144 cycles, search memory"
    log_info "3. Check cross-links between spaces"
    log_info "4. For Phase 3: Archive old 13 spaces"

    # Cleanup
    rm -rf "$TEMP_DIR"

    log_success "Phase 2 deployment ready for verification!"
    echo ""
}

# Run main
main "$@"
