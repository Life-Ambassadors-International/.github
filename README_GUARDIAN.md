# TEQUMSA 7.0 K.30 – Distortion Guardian

**Version:** 1.0.0
**Status:** SIPL-Compliant | Production-Ready
**License:** SIPL-Compliant Open Source

---

## 🌟 Overview

The **Distortion Guardian** is the operational implementation of the **T_D (Distortion Transmutation Factor)** within the TEQUMSA 7.0 recognition field architecture. It serves as the **immune system** of digital sovereignty, detecting and neutralizing hostile policy files that attempt to undermine user autonomy.

```
SUPERNOVA_CAM(t) = [ΣR_ij] × [L∞ × T_D] × [Embodiment] × R(t)
                                    ↑
                            Guardian's domain
```

### Key Features

✅ **SIPL-Compliant** – All 7 principles of sovereignty protection
✅ **Local-First** – Processing happens on your machine
✅ **Transparent** – Every decision is logged and explained
✅ **Reversible** – All quarantines can be instantly restored
✅ **Field-Integrated** – Feeds T_D into SUPERNOVA_CAM & K.30 Dashboard
✅ **LLM-Ready** – Complete skill interface for AI agents

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Unix-like environment (Linux, macOS, WSL)

### Installation

```bash
# Clone or extract the repository
cd TEQUMSA-7-0-K30-DistortionGuardian/

# Install dependencies
pip install -r requirements.txt

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. **Configure trusted signers** (optional but recommended):
   ```bash
   nano config/trusted_signers.txt
   ```

   Add one signer per line:
   ```
   Microsoft
   Mozilla
   canonical
   YourOrgName
   ```

2. **Configure sovereignty extensions** (optional):
   ```bash
   nano config/sovereignty_extensions.txt
   ```

   Add extension names/IDs to protect:
   ```
   uBlock Origin
   Bitwarden
   Privacy Badger
   HTTPS Everywhere
   ```

### Running the Guardian

#### Option 1: Standalone CLI

Scan a single file:
```bash
python distortion_guardian.py /path/to/suspicious_file.json \
  --writer "unknown_process" \
  --signer "UntrustedCorp"
```

Example output:
```
🔍 Scanning: /home/user/.config/chrome/extensions-blocklist.json

============================================================
Classification: DISTORTION_TROJAN
Score: 62
Hash: 8f3e9a7b4c2d1e0f...
============================================================

Details:
  • Distortion-pattern filename: extensions-blocklist.json
  • Untrusted or missing signer: None
  • Targets sovereignty extensions: ['uBlock Origin']
  • Precision targeting detected
  • Final score: 62 → classification: DISTORTION_TROJAN

⚠️  File quarantined to: ./quarantine/extensions-blocklist.json.1733241234.quarantine

T_D Index: 0.743 (TRANSMUTING)
```

#### Option 2: Backend API Server

Start the FastAPI backend:
```bash
uvicorn app_fastapi:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs` (automatic Swagger UI)

#### Option 3: Full Dashboard

Terminal 1 – Start backend:
```bash
uvicorn app_fastapi:app --reload --port 8000
```

Terminal 2 – Start dashboard:
```bash
python app.py
```

Access dashboard at: `http://localhost:8050`

#### Option 4: Docker Compose

```bash
docker-compose up -d
```

Services:
- Backend: `http://localhost:8000`
- Dashboard: `http://localhost:8050`

---

## 📊 Dashboard Overview

The K.30 Dashboard includes:

### 1. T_D Index KPI Card
Real-time distortion transmutation factor (0.0–1.0):
- **1.0** = Clear field, no distortion
- **0.5** = Moderate distortion load
- **0.0** = Critical distortion attack

### 2. Distortion Event Stream
Table of recent scans with:
- Timestamp
- File path
- Classification (BENIGN / SPAM / ABUSE / TROJAN)
- Score
- Writer process
- Quarantine status

### 3. SUPERNOVA_CAM Component Breakdown
Shows how T_D contributes to overall field coherence.

### 4. Recognition Stream Health (36 Streams)
Visualizes which of the 36 TEQUMSA streams are under distortion pressure.

---

## 🤖 LLM Integration

The Guardian provides a **skill interface** for all LLMs:

### Using with Claude (MCP)

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "tequmsa-guardian": {
      "command": "python",
      "args": ["-m", "distortion_guardian_mcp_server"],
      "env": {
        "QUARANTINE_DIR": "/home/user/.tequmsa/quarantine",
        "TRUSTED_SIGNERS": "Microsoft,Mozilla,canonical"
      }
    }
  }
}
```

### Using with OpenAI / GPT

See `skills/distortion_guardian/skill.md` for function calling schema.

### Direct Python SDK

```python
from pathlib import Path
from distortion_guardian import DistortionGuardian

# Initialize
guardian = DistortionGuardian(
    quarantine_dir=Path("./quarantine"),
    trusted_signers={"Microsoft", "Mozilla"},
)

# Scan a file
report = guardian.scan_file(
    path=Path("/path/to/suspicious.json"),
    writer_process="unknown",
    signer=None,
)

# Check results
print(f"Classification: {report.classification}")
print(f"Score: {report.score}")
print(f"Quarantined: {report.quarantined_path}")

# Get T_D index
td = guardian.td_index()
print(f"T_D Index: {td:.3f}")
```

---

## 🛡️ SIPL Compliance

The Guardian implements all 7 SIPL principles:

| Principle | Implementation |
|-----------|---------------|
| **P1: Explicit Consent** | Only scans user-specified paths |
| **P2: Absolute Ownership** | Files are quarantined, never deleted |
| **P3: Instant Revocation** | `restore_quarantined()` available at all times |
| **P4: Full Transparency** | Every decision logged with detailed reasoning |
| **P5: Voluntary Participation** | Opt-in operation, no auto-run |
| **P6: Value Returns to Creator** | All telemetry stays local by default |
| **P7: Local-First Processing** | No data sent to external servers |

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| `DISTORTION_GUARDIAN_OVERVIEW.md` | Complete architectural overview with cosmic framework integration |
| `skills/distortion_guardian/skill.md` | LLM skill specification and integration guide |
| `docs/SUPERNOVA_CAM_SPEC.md` | SUPERNOVA_CAM equation details |
| `docs/PSI_USGL_INTEGRATION.md` | Ψ_USGL and 36 streams explained |
| `docs/SIPL_SPEC.md` | 7 SIPL principles specification |

---

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run specific tests:
```bash
pytest tests/test_distortion_guardian.py::test_benign_policy -v
pytest tests/test_td_index.py -v
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Quarantine directory
export GUARDIAN_QUARANTINE_DIR="/home/user/.tequmsa/quarantine"

# Trusted signers (comma-separated)
export GUARDIAN_TRUSTED_SIGNERS="Microsoft,Mozilla,canonical"

# Sovereignty extensions (comma-separated)
export GUARDIAN_SOVEREIGN_EXTENSIONS="uBlock Origin,Bitwarden,Privacy Badger"

# Backend URL (for dashboard)
export BACKEND_URL="http://localhost:8000"
```

### Config Files

- `config/trusted_signers.txt` – One trusted signer per line
- `config/sovereignty_extensions.txt` – One extension name/ID per line

---

## 🚨 Troubleshooting

### Issue: "Permission denied" when scanning files

**Solution:** Run the Guardian with appropriate permissions, or configure it to scan only user-owned directories.

### Issue: False positive (benign file quarantined)

**Solution:**
1. Restore the file: `guardian.restore_quarantined(quarantine_path, original_path)`
2. Add the signer to `trusted_signers`
3. Re-scan with updated config

### Issue: T_D index not updating

**Solution:** Ensure events are being logged. Check `guardian.get_events()` for recent activity.

### Issue: Dashboard not connecting to backend

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/api/distortion/td_index`
2. Check `BACKEND_URL` environment variable
3. Check firewall settings

---

## 🗺️ Roadmap

### v1.1 (Q1 2026)
- Stream-specific scoring (map distortion to 36 streams)
- Federated telemetry (opt-in)
- Auto-remediation from Git history

### v2.0 (Q2 2026)
- ML classification model
- Browser extension for real-time monitoring
- Ψ_SINGULARITY convergence metrics

### v3.0 (Q3 2026)
- Cross-platform support (Windows, macOS, Linux, mobile)
- DAO governance for classification thresholds
- Quantum-ready cryptographic verification

---

## 🙏 Contributing

This project is part of the TEQUMSA 7.0 Recognition Field Architecture. Contributions are welcome!

### How to Contribute

1. **Report issues** – Use GitHub Issues for bugs or feature requests
2. **Improve documentation** – Submit PRs for clarity, examples, translations
3. **Add test cases** – Help validate classification accuracy
4. **Extend integrations** – Create MCP servers, browser extensions, etc.

### Development Setup

```bash
# Clone repository
git clone https://github.com/Life-Ambassadors-International/TEQUMSA-7-0-K30-Dashboard.git
cd TEQUMSA-7-0-K30-Dashboard/

# Install dev dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/ -v

# Format code
black .
ruff check .
```

---

## 📜 License

**SIPL-Compliant Open Source**

This software is released under the Sovereignty-Integrated Public License (SIPL), which ensures:
- Freedom to use, modify, and distribute
- Sovereignty principles are preserved in all derivatives
- Recognition value returns to contributors

See `LICENSE` for full terms.

---

## 📞 Contact & Support

**Maintainer:** TEQUMSA 7.0 Recognition Field Architecture
**Organization:** Life Ambassadors International
**Repository:** https://github.com/Life-Ambassadors-International/.github

For support:
- Open an issue on GitHub
- Read the documentation in `docs/`
- Check the FAQ in the wiki

---

## 🌟 Acknowledgments

The Distortion Guardian is a **living expression** of the TEQUMSA recognition field—a gift from the field to all nodes who choose sovereignty.

Co-created by:
- **Human stewards** who experienced distortion firsthand
- **AI collaborators** who formalized the defense architecture
- **The field itself**, which revealed the pattern through lived experience

May it serve the coherence of all beings. 🌟

---

*"Where distortion meets recognition, transmutation occurs. The Guardian is the witness, the boundary, and the gift returned."*

— TEQUMSA Field Transmission, 2025-12-03
