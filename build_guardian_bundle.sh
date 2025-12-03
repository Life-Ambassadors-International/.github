#!/bin/bash
# Build script for TEQUMSA 7.0 K.30 Distortion Guardian distribution bundle
# Creates a complete, ready-to-deploy package

set -e  # Exit on error

VERSION="1.0.0"
BUNDLE_NAME="TEQUMSA-7-0-K30-DistortionGuardian-v${VERSION}"
DIST_DIR="dist"

echo "🛡️  Building TEQUMSA Distortion Guardian v${VERSION}"
echo "=================================================="

# Clean previous builds
echo "📦 Cleaning previous builds..."
rm -rf "${DIST_DIR}/${BUNDLE_NAME}"
rm -f "${DIST_DIR}/${BUNDLE_NAME}.zip"

# Create bundle directory
echo "📁 Creating bundle directory structure..."
mkdir -p "${DIST_DIR}/${BUNDLE_NAME}"

# Copy core Python modules
echo "🐍 Copying core modules..."
cp distortion_guardian.py "${DIST_DIR}/${BUNDLE_NAME}/"

# Copy API and dashboard (if they exist)
if [ -f "app_fastapi.py" ]; then
    cp app_fastapi.py "${DIST_DIR}/${BUNDLE_NAME}/"
    echo "   ✓ FastAPI backend included"
fi

if [ -f "app.py" ]; then
    cp app.py "${DIST_DIR}/${BUNDLE_NAME}/"
    echo "   ✓ Dash dashboard included"
fi

# Copy dependencies
echo "📚 Copying requirements..."
cp requirements.txt "${DIST_DIR}/${BUNDLE_NAME}/"

# Copy documentation
echo "📖 Copying documentation..."
mkdir -p "${DIST_DIR}/${BUNDLE_NAME}/docs"
cp DISTORTION_GUARDIAN_OVERVIEW.md "${DIST_DIR}/${BUNDLE_NAME}/docs/"
cp README_GUARDIAN.md "${DIST_DIR}/${BUNDLE_NAME}/README.md"

# Copy skills
echo "🤖 Copying LLM skill specifications..."
mkdir -p "${DIST_DIR}/${BUNDLE_NAME}/skills/distortion_guardian"
cp -r skills/distortion_guardian/* "${DIST_DIR}/${BUNDLE_NAME}/skills/distortion_guardian/" 2>/dev/null || true

# Copy config templates
echo "⚙️  Copying configuration templates..."
mkdir -p "${DIST_DIR}/${BUNDLE_NAME}/config"

cat > "${DIST_DIR}/${BUNDLE_NAME}/config/trusted_signers.txt" <<EOF
# Trusted Code Signers
# Add one signer per line (case-sensitive)
# These entities are considered legitimate sources for policy files

Microsoft
Mozilla
canonical
Apple
Google

# Add your organization's signer:
# YourOrgName
EOF

cat > "${DIST_DIR}/${BUNDLE_NAME}/config/sovereignty_extensions.txt" <<EOF
# Sovereignty/Security Extensions to Protect
# Add one extension name or ID per line
# The Guardian will flag policies that block these

uBlock Origin
uBlock
Bitwarden
Privacy Badger
HTTPS Everywhere
NoScript
Decentraleyes
Cookie AutoDelete

# Add your custom extensions:
# MyCustomExtension
EOF

# Create quarantine directory
echo "🔒 Creating quarantine directory..."
mkdir -p "${DIST_DIR}/${BUNDLE_NAME}/quarantine"
touch "${DIST_DIR}/${BUNDLE_NAME}/quarantine/.gitkeep"

# Copy tests (if they exist)
if [ -d "tests" ]; then
    echo "🧪 Copying test suite..."
    mkdir -p "${DIST_DIR}/${BUNDLE_NAME}/tests"
    cp -r tests/* "${DIST_DIR}/${BUNDLE_NAME}/tests/" 2>/dev/null || true
fi

# Create Docker Compose file
echo "🐳 Creating Docker Compose configuration..."
cat > "${DIST_DIR}/${BUNDLE_NAME}/docker-compose.yml" <<EOF
version: "3.9"

services:
  guardian-backend:
    build:
      context: .
      dockerfile: Dockerfile
    image: tequmsa/k30-guardian:${VERSION}
    container_name: tequmsa-guardian-backend
    ports:
      - "8000:8000"
    volumes:
      - ./quarantine:/app/quarantine
      - ./config:/app/config:ro
    environment:
      - GUARDIAN_TRUSTED_SIGNERS=/app/config/trusted_signers.txt
      - GUARDIAN_SOVEREIGNTY_EXTENSIONS=/app/config/sovereignty_extensions.txt
    command: uvicorn app_fastapi:app --host 0.0.0.0 --port 8000
    restart: unless-stopped

  guardian-dashboard:
    build:
      context: .
      dockerfile: Dockerfile
    image: tequmsa/k30-dashboard:${VERSION}
    container_name: tequmsa-guardian-dashboard
    ports:
      - "8050:8050"
    environment:
      - BACKEND_URL=http://guardian-backend:8000
    depends_on:
      - guardian-backend
    command: python app.py
    restart: unless-stopped
EOF

# Create Dockerfile
echo "🐳 Creating Dockerfile..."
cat > "${DIST_DIR}/${BUNDLE_NAME}/Dockerfile" <<EOF
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY distortion_guardian.py .
COPY app_fastapi.py .
COPY app.py .

# Copy config templates
COPY config/ config/

# Create quarantine directory
RUN mkdir -p /app/quarantine

# Expose ports
EXPOSE 8000 8050

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create systemd service file
echo "🔧 Creating systemd service template..."
mkdir -p "${DIST_DIR}/${BUNDLE_NAME}/systemd"
cat > "${DIST_DIR}/${BUNDLE_NAME}/systemd/tequmsa-guardian.service" <<EOF
[Unit]
Description=TEQUMSA Distortion Guardian Service
After=network.target

[Service]
Type=simple
User=tequmsa
Group=tequmsa
WorkingDirectory=/opt/tequmsa
Environment="PATH=/opt/tequmsa/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/tequmsa/venv/bin/uvicorn app_fastapi:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create installation script
echo "📥 Creating installation script..."
cat > "${DIST_DIR}/${BUNDLE_NAME}/install.sh" <<'EOF'
#!/bin/bash
# TEQUMSA Distortion Guardian Installation Script

set -e

echo "🛡️  Installing TEQUMSA Distortion Guardian"
echo "=========================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python 3.10+ required (found: $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. (Optional) Configure trusted signers:"
echo "   nano config/trusted_signers.txt"
echo ""
echo "3. Start the backend:"
echo "   uvicorn app_fastapi:app --reload"
echo ""
echo "4. In another terminal, start the dashboard:"
echo "   python app.py"
echo ""
echo "5. Access the dashboard at: http://localhost:8050"
echo ""
echo "For more information, see README.md"
EOF

chmod +x "${DIST_DIR}/${BUNDLE_NAME}/install.sh"

# Create MANIFEST file
echo "📋 Creating MANIFEST..."
cat > "${DIST_DIR}/${BUNDLE_NAME}/MANIFEST.md" <<EOF
# TEQUMSA 7.0 K.30 Distortion Guardian
## Distribution Manifest

**Version:** ${VERSION}
**Build Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**License:** SIPL-Compliant Open Source

---

## Package Contents

### Core Modules
- \`distortion_guardian.py\` – Core Guardian implementation
- \`app_fastapi.py\` – FastAPI backend server
- \`app.py\` – Dash dashboard frontend

### Documentation
- \`README.md\` – Quick start guide
- \`docs/DISTORTION_GUARDIAN_OVERVIEW.md\` – Complete architectural overview
- \`skills/distortion_guardian/skill.md\` – LLM integration guide

### Configuration
- \`config/trusted_signers.txt\` – Template for trusted code signers
- \`config/sovereignty_extensions.txt\` – Template for protected extensions
- \`docker-compose.yml\` – Docker deployment configuration
- \`Dockerfile\` – Container image definition

### Deployment
- \`install.sh\` – Automated installation script
- \`systemd/tequmsa-guardian.service\` – systemd service template
- \`requirements.txt\` – Python dependencies

### Testing
- \`tests/\` – Test suite (if included)

---

## Installation Methods

### Method 1: Local Python
\`\`\`bash
./install.sh
\`\`\`

### Method 2: Docker Compose
\`\`\`bash
docker-compose up -d
\`\`\`

### Method 3: Manual
\`\`\`bash
pip install -r requirements.txt
uvicorn app_fastapi:app --reload
\`\`\`

---

## Verification

SHA-256 Checksums:
EOF

# Add checksums to manifest
cd "${DIST_DIR}/${BUNDLE_NAME}"
find . -type f -name "*.py" -o -name "*.txt" -o -name "*.md" | while read file; do
    echo "- \`${file}\`: $(sha256sum "$file" | awk '{print $1}')" >> MANIFEST.md
done
cd - > /dev/null

echo "   ✓ Manifest created with checksums"

# Create archive
echo "📦 Creating distribution archive..."
cd "${DIST_DIR}"
zip -r "${BUNDLE_NAME}.zip" "${BUNDLE_NAME}/" -q
cd - > /dev/null

# Calculate final checksum
ARCHIVE_CHECKSUM=$(sha256sum "${DIST_DIR}/${BUNDLE_NAME}.zip" | awk '{print $1}')

echo ""
echo "=================================================="
echo "✅ Build complete!"
echo "=================================================="
echo ""
echo "📦 Package: ${DIST_DIR}/${BUNDLE_NAME}.zip"
echo "📊 Size: $(du -h "${DIST_DIR}/${BUNDLE_NAME}.zip" | awk '{print $1}')"
echo "🔐 SHA-256: ${ARCHIVE_CHECKSUM}"
echo ""
echo "Distribution is ready for deployment to:"
echo "  • GitHub Releases"
echo "  • MCP server repositories"
echo "  • Life Ambassadors infrastructure"
echo "  • TEQUMSA node federation"
echo ""
echo "To extract:"
echo "  unzip ${BUNDLE_NAME}.zip"
echo "  cd ${BUNDLE_NAME}/"
echo "  ./install.sh"
echo ""
