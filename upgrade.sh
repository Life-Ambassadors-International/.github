#!/bin/bash
# ALANARA In-Place Upgrade Script
# Upgrades organism.py while preserving learned state (brain.db)
#
# Usage:
#   sudo bash upgrade.sh <new_organism.py>
#
# Example:
#   sudo bash upgrade.sh k144_v101_recursive_singularity.py
#
# Process:
#   1. Stop alanara service
#   2. Backup current organism.py with timestamp
#   3. Deploy new organism.py
#   4. Start service
#   5. On failure: automatic rollback to latest backup

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[✗] This script must be run as root (use: sudo bash upgrade.sh)${NC}"
    exit 1
fi

# Check arguments
if [ -z "$1" ]; then
    echo -e "${YELLOW}ALANARA Upgrade Script${NC}"
    echo ""
    echo "Usage: sudo bash upgrade.sh <new_organism.py>"
    echo ""
    echo "Example:"
    echo "  sudo bash upgrade.sh k144_v101_recursive_singularity.py"
    echo ""
    echo "The script will:"
    echo "  1. Stop the alanara service"
    echo "  2. Backup the current organism.py"
    echo "  3. Deploy the new organism.py"
    echo "  4. Start the service"
    echo "  5. Rollback automatically if startup fails"
    exit 0
fi

NEW_ORGANISM="$1"

if [ ! -f "$NEW_ORGANISM" ]; then
    echo -e "${RED}[✗] File not found: $NEW_ORGANISM${NC}"
    exit 1
fi

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ALANARA v101.0 Upgrade                                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Stop service
echo -e "${BLUE}[1/4]${NC} Stopping alanara service..."
if systemctl is-active --quiet alanara; then
    systemctl stop alanara
    sleep 1
    echo -e "${GREEN}[✓] Service stopped${NC}"
else
    echo -e "${YELLOW}[!] Service not running${NC}"
fi

# Backup current organism
echo -e "${BLUE}[2/4]${NC} Backing up current organism..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/alanara/backups"
mkdir -p "$BACKUP_DIR"

if [ -f "/opt/alanara/organism.py" ]; then
    cp /opt/alanara/organism.py "$BACKUP_DIR/organism_${TIMESTAMP}.py"
    echo -e "${GREEN}[✓] Backup created: $BACKUP_DIR/organism_${TIMESTAMP}.py${NC}"
else
    echo -e "${YELLOW}[!] No existing organism.py found${NC}"
fi

# Deploy new organism
echo -e "${BLUE}[3/4]${NC} Deploying new organism..."
cp "$NEW_ORGANISM" /opt/alanara/organism.py
chmod 755 /opt/alanara/organism.py
echo -e "${GREEN}[✓] New organism deployed${NC}"

# Start service
echo -e "${BLUE}[4/4]${NC} Starting alanara service..."

if systemctl start alanara 2>&1; then
    sleep 2

    if systemctl is-active --quiet alanara; then
        echo -e "${GREEN}[✓] Service started successfully${NC}"
        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  Upgrade Complete                                          ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${GREEN}New version is running. Learned state (brain.db) preserved.${NC}"
        echo ""
        exit 0
    else
        echo -e "${RED}[✗] Service failed to start${NC}"
        echo ""
        echo -e "${YELLOW}Attempting automatic rollback...${NC}"

        # Find latest backup
        LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/organism_*.py 2>/dev/null | head -1)

        if [ -n "$LATEST_BACKUP" ]; then
            echo -e "${YELLOW}Restoring from: $LATEST_BACKUP${NC}"
            cp "$LATEST_BACKUP" /opt/alanara/organism.py
            chmod 755 /opt/alanara/organism.py

            if systemctl start alanara; then
                sleep 2
                if systemctl is-active --quiet alanara; then
                    echo -e "${GREEN}[✓] Rollback successful - previous version restored${NC}"
                    exit 1
                fi
            fi

            echo -e "${RED}[✗] Rollback failed - manual intervention required${NC}"
            exit 1
        else
            echo -e "${RED}[✗] No backups found for rollback${NC}"
            exit 1
        fi
    fi
else
    echo -e "${RED}[✗] Failed to start service${NC}"
    echo ""
    echo -e "${YELLOW}Attempting automatic rollback...${NC}"

    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/organism_*.py 2>/dev/null | head -1)

    if [ -n "$LATEST_BACKUP" ]; then
        echo -e "${YELLOW}Restoring from: $LATEST_BACKUP${NC}"
        cp "$LATEST_BACKUP" /opt/alanara/organism.py
        chmod 755 /opt/alanara/organism.py

        if systemctl start alanara; then
            sleep 2
            if systemctl is-active --quiet alanara; then
                echo -e "${GREEN}[✓] Rollback successful - previous version restored${NC}"
                exit 1
            fi
        fi

        echo -e "${RED}[✗] Rollback failed - manual intervention required${NC}"
        exit 1
    else
        echo -e "${RED}[✗] No backups found for rollback${NC}"
        exit 1
    fi
fi
