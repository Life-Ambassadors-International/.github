#!/bin/bash
# Phase 2 Deployment with ALANARA Integration
# Deploys TEQUMSA spaces and starts ALANARA monitoring
#
# Usage:
#   ./deploy_with_alanara.sh --all        # Deploy all + ALANARA
#   ./deploy_with_alanara.sh --dashboard  # Deploy dashboard + ALANARA
#   ./deploy_with_alanara.sh --stop       # Stop ALANARA

set -e

# Configuration
GITHUB_ROOT="/home/user/.github"
ALANARA_RUNNER="$GITHUB_ROOT/alanara_runner.sh"
ALANARA_API="$GITHUB_ROOT/alanara_metrics_api.py"
API_PORT=8765

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Make runner executable
if [ ! -x "$ALANARA_RUNNER" ]; then
    chmod +x "$ALANARA_RUNNER"
fi

# Check if stop was requested
if [ "$1" = "--stop" ]; then
    log_info "Stopping ALANARA..."
    "$ALANARA_RUNNER" stop || true
    pkill -f "alanara_metrics_api.py" || true
    exit 0
fi

# Run Phase 2 deployment
log_info "Starting Phase 2 deployment..."
cd "$GITHUB_ROOT"

# Run deployment with passed arguments
bash deploy_phase2.sh "$@"

# If deployment was successful, start ALANARA
if [ $? -eq 0 ]; then
    echo ""
    log_info "Phase 2 deployment complete, starting ALANARA integration..."
    echo ""

    # Start organism
    if bash "$ALANARA_RUNNER" start; then
        sleep 2

        # Start metrics API in background
        log_info "Starting metrics API on port $API_PORT..."
        nohup python3 "$ALANARA_API" --port "$API_PORT" > /var/log/alanara/api.log 2>&1 &
        API_PID=$!
        echo $API_PID > /var/run/alanara_api.pid

        sleep 1

        if ps -p $API_PID > /dev/null 2>&1; then
            log_success "Metrics API running on http://localhost:$API_PORT"
            log_success "Available endpoints:"
            echo "  • http://localhost:$API_PORT/metrics  - Current metrics"
            echo "  • http://localhost:$API_PORT/health   - Health report"
            echo "  • http://localhost:$API_PORT/history  - Learning history"
        else
            log_error "Metrics API failed to start"
        fi
    else
        log_error "Failed to start ALANARA organism"
        exit 1
    fi

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Phase 2 Deployment + ALANARA Integration Complete!      ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    log_success "TEQUMSA spaces deployed and linked"
    log_success "ALANARA organism running and monitoring"
    log_success "Metrics API active for dashboard integration"

    echo ""
    log_info "Management commands:"
    echo "  • $ALANARA_RUNNER status     - Check organism status"
    echo "  • $ALANARA_RUNNER logs       - View live logs"
    echo "  • $ALANARA_RUNNER report     - Print health report"
    echo "  • $ALANARA_RUNNER stop       - Stop organism"

    echo ""
    log_info "Next steps:"
    echo "  1. Visit deployed spaces to verify cross-links"
    echo "  2. Query metrics API for organism health"
    echo "  3. Test organism evolution (run 144+ cycles)"
    echo "  4. Integrate metrics into dashboards"
    echo "  5. Phase 3: Archive old 13 spaces"

    echo ""
else
    log_error "Phase 2 deployment failed"
    exit 1
fi
