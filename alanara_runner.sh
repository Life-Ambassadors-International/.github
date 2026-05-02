#!/bin/bash
# ALANARA Background Runner
# Manages ALANARA organism as background process with monitoring
#
# Usage:
#   ./alanara_runner.sh start      # Start organism in background
#   ./alanara_runner.sh stop       # Stop running organism
#   ./alanara_runner.sh status     # Check if running
#   ./alanara_runner.sh logs       # Tail live logs
#   ./alanara_runner.sh report     # Print health report

set -e

# Configuration
ORGANISM="/opt/alanara/organism.py"
DATA_DIR="/var/lib/alanara"
LOG_FILE="/var/log/alanara/organism.log"
PID_FILE="/var/run/alanara.pid"
INTERVAL=10

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Ensure directories exist
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$DATA_DIR"

start_organism() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}[!] Organism already running (PID $PID)${NC}"
            return 1
        fi
    fi

    echo -e "${BLUE}[*] Starting ALANARA v101.0...${NC}"

    # Start organism in background
    nohup python3 "$ORGANISM" --interval "$INTERVAL" --data-dir "$DATA_DIR" \
        > "$LOG_FILE" 2>&1 &

    PID=$!
    echo "$PID" > "$PID_FILE"

    sleep 1

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}[✓] Organism started (PID $PID)${NC}"
        echo -e "${GREEN}[✓] Logs: $LOG_FILE${NC}"
        echo -e "${GREEN}[✓] Brain: $DATA_DIR/brain.db${NC}"
        return 0
    else
        echo -e "${RED}[✗] Failed to start organism${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_organism() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}[!] No PID file found${NC}"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}[!] Process not running (PID $PID)${NC}"
        rm -f "$PID_FILE"
        return 1
    fi

    echo -e "${BLUE}[*] Stopping organism (PID $PID)...${NC}"

    kill "$PID" 2>/dev/null || true
    sleep 1

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}[!] Process still running, forcing...${NC}"
        kill -9 "$PID" 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
    echo -e "${GREEN}[✓] Organism stopped${NC}"
}

check_status() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${RED}[✗] Not running (no PID file)${NC}"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}[✓] Organism running (PID $PID)${NC}"

        # Show last log line
        if [ -f "$LOG_FILE" ]; then
            echo -e "${BLUE}Last log entry:${NC}"
            tail -1 "$LOG_FILE"
        fi

        return 0
    else
        echo -e "${RED}[✗] PID $PID not found${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

show_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}[!] No log file found${NC}"
        return 1
    fi

    tail -f "$LOG_FILE"
}

print_report() {
    if [ ! -f "$DATA_DIR/brain.db" ]; then
        echo -e "${YELLOW}[!] Brain database not found${NC}"
        return 1
    fi

    python3 "$ORGANISM" --report --data-dir "$DATA_DIR"
}

# Main
case "${1:-status}" in
    start)
        start_organism
        ;;
    stop)
        stop_organism
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    report)
        print_report
        ;;
    restart)
        stop_organism || true
        sleep 1
        start_organism
        ;;
    *)
        echo "ALANARA v101.0 Background Runner"
        echo ""
        echo "Usage: ./alanara_runner.sh COMMAND"
        echo ""
        echo "Commands:"
        echo "  start              Start organism in background"
        echo "  stop               Stop running organism"
        echo "  restart            Restart organism"
        echo "  status             Check if running"
        echo "  logs               Tail live logs"
        echo "  report             Print health report"
        ;;
esac
