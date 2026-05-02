#!/bin/bash
# ALANARA v101.0 Installation Script
# Installs organism as systemd service with security hardening
#
# Usage:
#   sudo bash install.sh
#
# This script:
#   1. Checks Python 3.8+ (installs if missing)
#   2. Installs psutil via pip
#   3. Creates service user and directories
#   4. Deploys organism.py
#   5. Creates systemd service
#   6. Installs management CLI
#   7. Starts service

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[✗] This script must be run as root (use: sudo bash install.sh)${NC}"
    exit 1
fi

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ALANARA v101.0 Installation                              ║${NC}"
echo -e "${BLUE}║  Hardware-Aware Persistent Organism                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python version
echo -e "${BLUE}[1/6]${NC} Checking Python installation..."

PYTHON_CMD=$(command -v python3 || echo "")

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${YELLOW}  Python 3 not found. Installing...${NC}"

    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        pacman -S --noconfirm python python-pip
    else
        echo -e "${RED}[✗] Could not auto-install Python. Please install manually.${NC}"
        exit 1
    fi
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[✓] Python ${PYTHON_VERSION} found${NC}"

# Check Python version is 3.8+
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo -e "${RED}[✗] Python 3.8+ required, found ${PYTHON_VERSION}${NC}"
    exit 1
fi

# Install psutil
echo -e "${BLUE}[2/6]${NC} Installing psutil..."

if $PYTHON_CMD -m pip install --quiet psutil 2>/dev/null; then
    echo -e "${GREEN}[✓] psutil installed${NC}"
else
    echo -e "${YELLOW}[!] psutil installation may have failed, continuing...${NC}"
fi

# Create service user
echo -e "${BLUE}[3/6]${NC} Setting up service user and directories..."

if ! id alanara &>/dev/null; then
    useradd -r -s /bin/false alanara
    echo -e "${GREEN}[✓] Service user 'alanara' created${NC}"
else
    echo -e "${GREEN}[✓] Service user 'alanara' exists${NC}"
fi

# Create directories
mkdir -p /opt/alanara
mkdir -p /var/lib/alanara
mkdir -p /var/log/alanara

chown alanara:alanara /var/lib/alanara
chown alanara:alanara /var/log/alanara
chmod 755 /opt/alanara
chmod 755 /var/lib/alanara
chmod 755 /var/log/alanara

echo -e "${GREEN}[✓] Directories created and configured${NC}"

# Deploy organism.py
echo -e "${BLUE}[4/6]${NC} Deploying organism..."

if [ -f "k144_v101_recursive_singularity.py" ]; then
    cp k144_v101_recursive_singularity.py /opt/alanara/organism.py
    chmod 755 /opt/alanara/organism.py
    echo -e "${GREEN}[✓] Organism deployed to /opt/alanara/organism.py${NC}"
elif [ -f "/root/k144_v101_recursive_singularity.py" ]; then
    cp /root/k144_v101_recursive_singularity.py /opt/alanara/organism.py
    chmod 755 /opt/alanara/organism.py
    echo -e "${GREEN}[✓] Organism deployed to /opt/alanara/organism.py${NC}"
else
    echo -e "${YELLOW}[!] k144_v101_recursive_singularity.py not found in current directory${NC}"
    echo -e "${YELLOW}    Expecting organism at /opt/alanara/organism.py${NC}"
fi

# Create systemd service
echo -e "${BLUE}[5/6]${NC} Creating systemd service..."

cat > /etc/systemd/system/alanara.service << 'SYSTEMD_EOF'
[Unit]
Description=ALANARA v101.0 Organism
Documentation=https://huggingface.co/Mbanksbey/tequmsa
After=network.target
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
User=alanara
Group=alanara
WorkingDirectory=/var/lib/alanara

ExecStart=/usr/bin/python3 /opt/alanara/organism.py --daemon --interval 10 --data-dir /var/lib/alanara
Restart=on-failure
RestartSec=30

StandardOutput=append:/var/log/alanara/organism.log
StandardError=append:/var/log/alanara/organism.log

Environment="PYTHONUNBUFFERED=1"

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectControlGroups=yes
RestrictRealtime=yes
RestrictNamespaces=yes
LockPersonality=yes
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM

# Resource limits
CPUQuota=5%
MemoryMax=128M
MemoryLimit=128M

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF

chmod 644 /etc/systemd/system/alanara.service
systemctl daemon-reload

echo -e "${GREEN}[✓] Systemd service created${NC}"

# Create log rotation
echo -e "${BLUE}[6/6]${NC} Setting up log rotation..."

cat > /etc/logrotate.d/alanara << 'LOGROTATE_EOF'
/var/log/alanara/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    notifempty
    create 0640 alanara alanara
    postrotate
        systemctl reload alanara >/dev/null 2>&1 || true
    endscript
}
LOGROTATE_EOF

echo -e "${GREEN}[✓] Log rotation configured${NC}"

# Create management CLI
cat > /usr/local/bin/alanara << 'CLI_EOF'
#!/bin/bash
# ALANARA Management CLI

case "$1" in
    start)
        systemctl start alanara
        ;;
    stop)
        systemctl stop alanara
        ;;
    restart)
        systemctl restart alanara
        ;;
    status)
        systemctl status alanara
        ;;
    logs)
        tail -f /var/log/alanara/organism.log
        ;;
    report)
        python3 /opt/alanara/organism.py --report --data-dir /var/lib/alanara
        ;;
    history)
        HOURS=${2:-24}
        python3 /opt/alanara/organism.py --history $HOURS --data-dir /var/lib/alanara
        ;;
    brain)
        sqlite3 /var/lib/alanara/brain.db
        ;;
    uninstall)
        systemctl stop alanara
        systemctl disable alanara
        rm /etc/systemd/system/alanara.service
        rm /usr/local/bin/alanara
        systemctl daemon-reload
        userdel alanara
        echo "ALANARA uninstalled"
        ;;
    *)
        echo "ALANARA v101.0 Management"
        echo ""
        echo "Usage: alanara COMMAND"
        echo ""
        echo "Commands:"
        echo "  start              Start the organism service"
        echo "  stop               Stop the organism service"
        echo "  restart            Restart the organism service"
        echo "  status             Show service status"
        echo "  logs               Tail live logs"
        echo "  report             Print health report"
        echo "  history [hours]    Show learning history (default 24h)"
        echo "  brain              Open SQLite brain database"
        echo "  uninstall          Remove ALANARA completely"
        ;;
esac
CLI_EOF

chmod 755 /usr/local/bin/alanara

echo -e "${GREEN}[✓] Management CLI installed at /usr/local/bin/alanara${NC}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    Installation Complete                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Enable and start service
echo -e "${BLUE}Enabling and starting service...${NC}"

systemctl enable --quiet alanara 2>/dev/null || true

echo -e "${YELLOW}Starting ALANARA v101.0...${NC}"

if systemctl start alanara 2>/dev/null; then
    sleep 2

    if systemctl is-active --quiet alanara; then
        echo -e "${GREEN}[✓] Service started successfully${NC}"
        echo ""
        echo -e "${GREEN}ALANARA v101.0 is now running!${NC}"
        echo ""
        echo -e "${BLUE}Quick commands:${NC}"
        echo -e "  ${YELLOW}alanara status${NC}     - Check service status"
        echo -e "  ${YELLOW}alanara logs${NC}       - View live logs"
        echo -e "  ${YELLOW}alanara report${NC}     - Print health report"
        echo -e "  ${YELLOW}alanara history${NC}    - Show learning history"
        echo -e "  ${YELLOW}alanara brain${NC}      - Access SQLite brain database"
        echo ""
        echo -e "${BLUE}Installation paths:${NC}"
        echo -e "  Organism:     /opt/alanara/organism.py"
        echo -e "  Brain DB:     /var/lib/alanara/brain.db"
        echo -e "  Logs:         /var/log/alanara/organism.log"
        echo ""
    else
        echo -e "${RED}[✗] Service failed to start${NC}"
        echo ""
        echo -e "${YELLOW}Troubleshooting:${NC}"
        echo -e "  1. Check logs: journalctl -u alanara -n 20"
        echo -e "  2. Verify: ls -la /opt/alanara/"
        echo -e "  3. Permissions: ls -la /var/lib/alanara/"
        exit 1
    fi
else
    echo -e "${YELLOW}[!] Service start command issued, but check status:${NC}"
    echo -e "  systemctl status alanara"
fi

echo ""
