# TEQUMSA 7.0 K.30 Distortion Guardian
## Repository Structure Documentation

**Version:** 1.0.0
**Last Updated:** 2025-12-03

---

## Overview

This document describes the complete repository structure for the TEQUMSA Distortion Guardian project, including all files, directories, and their purposes within the cosmic framework.

---

## Directory Tree

```
TEQUMSA-7-0-K30-DistortionGuardian/
│
├── README_GUARDIAN.md                    # Quick start guide
├── DISTORTION_GUARDIAN_OVERVIEW.md       # Complete cosmic framework overview
├── REPO_STRUCTURE.md                     # This file
├── requirements.txt                      # Python dependencies
├── build_guardian_bundle.sh              # Build script for distribution
│
├── distortion_guardian.py                # Core Guardian module
├── app_fastapi.py                        # FastAPI backend server
├── app.py                                # Dash dashboard frontend
│
├── config/                               # Configuration files
│   ├── trusted_signers.txt               # List of trusted code signers
│   └── sovereignty_extensions.txt        # Protected extension names/IDs
│
├── docs/                                 # Documentation
│   ├── DISTORTION_GUARDIAN_OVERVIEW.md   # Main architectural overview
│   ├── TEQUMSA_FIELD_ARCHITECTURE.md     # Field theory documentation
│   ├── SUPERNOVA_CAM_SPEC.md             # SUPERNOVA_CAM equation spec
│   ├── PSI_USGL_INTEGRATION.md           # Ψ_USGL & 36 streams guide
│   └── SIPL_SPEC.md                      # 7 SIPL principles specification
│
├── skills/                               # LLM skill specifications
│   └── distortion_guardian/
│       ├── skill.md                      # Main skill specification
│       └── examples/
│           ├── scan_browser_profile.md
│           ├── interpret_trojan_report.md
│           └── restore_quarantined_file.md
│
├── quarantine/                           # Runtime quarantine directory
│   └── .gitkeep                          # Preserve empty directory in git
│
├── tests/                                # Test suite
│   ├── test_distortion_guardian.py       # Core module tests
│   ├── test_td_index.py                  # T_D index computation tests
│   ├── test_api.py                       # FastAPI endpoint tests
│   └── fixtures/                         # Test data
│       ├── benign_policy.json
│       ├── hostile_blocklist.json
│       ├── corp_managed_policy.json
│       └── malformed_policy.json
│
├── systemd/                              # System service configurations
│   └── tequmsa-guardian.service          # systemd service template
│
├── docker-compose.yml                    # Docker deployment config
├── Dockerfile                            # Container image definition
├── .dockerignore                         # Docker build exclusions
│
├── .gitignore                            # Git exclusions
├── LICENSE                               # SIPL license text
│
└── dist/                                 # Build artifacts (not in git)
    └── TEQUMSA-7-0-K30-DistortionGuardian-v1.0.0.zip
```

---

## File Descriptions

### Root Level

#### `README_GUARDIAN.md`
Quick start guide for users. Includes:
- Installation instructions
- Usage examples
- Configuration guide
- Troubleshooting
- Links to detailed docs

#### `DISTORTION_GUARDIAN_OVERVIEW.md`
**The main architectural document** that ties the Guardian into the cosmic TEQUMSA framework:
- Ψ_USGL integration
- Ψ_SINGULARITY connection
- 36 recognition streams mapping
- SUPERNOVA_CAM T_D implementation
- Module architecture
- Dashboard integration
- Full cosmic language explanation

#### `REPO_STRUCTURE.md`
This file. Documents the repository layout and file purposes.

#### `requirements.txt`
Python package dependencies:
- FastAPI (backend)
- Dash (dashboard)
- Pydantic (data validation)
- Testing frameworks
- Code quality tools

#### `build_guardian_bundle.sh`
Automated build script that creates a distributable `.zip` package containing:
- All source files
- Documentation
- Config templates
- Installation scripts
- Docker configs
- Checksums for verification

---

### Core Modules

#### `distortion_guardian.py`
**The heart of the system.** Contains:

**Classes:**
- `DistortionClass` – Enum for classification taxonomy
- `DistortionReport` – Data class for scan results
- `DistortionGuardian` – Main guardian logic

**Key Methods:**
- `scan_file()` – Detect and classify distortion patterns
- `td_index()` – Compute T_D ∈ [0,1] for SUPERNOVA_CAM
- `to_tequmsa_event()` – Convert reports to field events
- `restore_quarantined()` – Implement SIPL P3 (revocation)

**Scoring Algorithm:**
Weighted heuristics across 5 dimensions:
1. Filename patterns (+0 to +15)
2. Path location (+0 to +10)
3. Provenance (+40 or -30)
4. Sovereignty targeting (+0 to +30)
5. Behavioral patterns (+5 to +20)

**Classification Thresholds:**
- `< 20` → BENIGN_POLICY
- `20-29` → DISTORTION_SPAM
- `30-49` → DISTORTION_POLICY_ABUSE
- `≥ 50` → DISTORTION_TROJAN (quarantine)

#### `app_fastapi.py`
FastAPI backend server exposing REST API:

**Endpoints:**
- `POST /api/distortion/scan_file` – Upload and scan a file
- `GET /api/distortion/events` – Retrieve event history + T_D
- `GET /api/distortion/td_index` – Get T_D scalar for SUPERNOVA_CAM
- `GET /api/distortion/stream_health` – 36 streams health status

**Integration:**
- Consumed by Dash dashboard
- Consumed by LLM agents via HTTP
- Can be deployed standalone or with dashboard

#### `app.py`
Dash dashboard frontend:

**Components:**
- T_D Index KPI card
- SUPERNOVA_CAM component breakdown
- Distortion event stream (table)
- Recognition stream health matrix (36 streams)
- Real-time updates (5-second refresh)

**Visualization:**
- Plotly graphs for T_D trends
- Color-coded classifications
- Interactive event details

---

### Configuration (`config/`)

#### `trusted_signers.txt`
Newline-separated list of code signers considered trustworthy:
```
Microsoft
Mozilla
canonical
YourOrgName
```

Files signed by these entities receive a **-30 score bonus** (trust).

#### `sovereignty_extensions.txt`
Newline-separated list of extension names/IDs to protect:
```
uBlock Origin
Bitwarden
Privacy Badger
```

Policies blocking these extensions receive a **+30 score penalty** (sovereignty violation).

---

### Documentation (`docs/`)

#### `DISTORTION_GUARDIAN_OVERVIEW.md`
The **master document** (also in root). Contains:
- Full cosmic framework integration
- Ψ_USGL, Ψ_SINGULARITY, 36 streams
- SUPERNOVA_CAM T_D implementation
- Module architecture with diagrams
- Dashboard integration
- LLM skill overview
- Repository layout
- Usage examples

**Target Audience:** Human + AI readers who need deep understanding of how T_D fits into TEQUMSA cosmology.

#### `TEQUMSA_FIELD_ARCHITECTURE.md`
Describes the overall TEQUMSA 7.0 recognition field:
- Field theory foundations
- Recognition streams
- Kardashev scaling
- Node federation
- Coherence metrics

#### `SUPERNOVA_CAM_SPEC.md`
Technical specification for the SUPERNOVA_CAM equation:
```
SUPERNOVA_CAM(t) = [ΣR_ij] × [L∞ × T_D] × [Embodiment] × R(t)
```
- Component definitions
- Calculation methodology
- Integration with Guardian's T_D
- Field event formats

#### `PSI_USGL_INTEGRATION.md`
Ψ_USGL (Universal Sovereign Grid Layer) guide:
- Quantum coherence substrate
- 36 recognition streams (6×6 matrix)
- How distortion attacks streams
- How Guardian protects Ψ_USGL

#### `SIPL_SPEC.md`
The 7 SIPL (Sovereignty-Integrated Public License) principles:
- P1: Explicit Consent Required
- P2: Absolute Ownership Preserved
- P3: Instant Revocation Available
- P4: Full Transparency Maintained
- P5: Voluntary Participation Only
- P6: Value Returns to Creator
- P7: Local-First Processing

Explains how each principle is enforced in Guardian code.

---

### Skills (`skills/distortion_guardian/`)

#### `skill.md`
**LLM skill specification** for AI agents (Claude, GPT, etc.):

**Contents:**
- Purpose and cosmic context
- SIPL compliance requirements
- API overview (5 core operations)
- Classification thresholds
- T_D index computation
- 36 streams integration
- Example workflows (3 detailed scenarios)
- Safety & limitations
- Integration patterns (MCP, function calling, SDK)
- Communication style guidelines
- Testing & validation criteria

**Target Audience:** LLMs that need to understand how to use the Guardian on behalf of users.

#### `examples/`
Detailed example scenarios:

**`scan_browser_profile.md`:**
Walkthrough of scanning user's browser profile for distortion files.

**`interpret_trojan_report.md`:**
How to explain a DISTORTION_TROJAN finding in natural language.

**`restore_quarantined_file.md`:**
Reversing a quarantine (SIPL P3 implementation).

---

### Quarantine (`quarantine/`)

Runtime directory where hostile files are moved:
- Files are preserved with original names + timestamp suffix
- Format: `original_name.json.1733241234.quarantine`
- User can inspect, restore, or delete
- Never automatically purged (SIPL P2: ownership)

`.gitkeep` ensures directory exists in version control but is empty.

---

### Tests (`tests/`)

#### `test_distortion_guardian.py`
Unit tests for core Guardian module:
- Test benign policy (should not quarantine)
- Test hostile blocklist (should quarantine)
- Test malformed JSON (should penalize)
- Test provenance scoring
- Test sovereignty targeting detection

#### `test_td_index.py`
Tests for T_D index computation:
- Empty event log → T_D = 1.0
- All benign events → T_D = 1.0
- All trojan events → T_D = 0.0
- Mixed events → T_D ∈ (0,1)
- Windowing behavior

#### `test_api.py`
Integration tests for FastAPI endpoints:
- POST file scan
- GET events
- GET T_D index
- Error handling

#### `fixtures/`
Test data files:
- `benign_policy.json` – Signed, broad policy
- `hostile_blocklist.json` – Unsigned, targets uBlock
- `corp_managed_policy.json` – Signed, moderate restrictions
- `malformed_policy.json` – Invalid JSON

---

### Deployment

#### `docker-compose.yml`
Multi-container deployment:
- `guardian-backend` service (FastAPI on port 8000)
- `guardian-dashboard` service (Dash on port 8050)
- Volume mounts for quarantine and config
- Environment variables for signers/extensions

#### `Dockerfile`
Container image definition:
- Based on `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Copies application files
- Exposes ports 8000 (API) and 8050 (dashboard)
- Default command: `uvicorn app_fastapi:app`

#### `systemd/tequmsa-guardian.service`
systemd service template for Linux deployments:
- Runs as dedicated `tequmsa` user
- Auto-restart on failure
- Logs to systemd journal
- Starts after network

**Installation:**
```bash
sudo cp systemd/tequmsa-guardian.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tequmsa-guardian
sudo systemctl start tequmsa-guardian
```

---

## Build and Distribution

### Building the Bundle

Run the build script:
```bash
./build_guardian_bundle.sh
```

This creates:
- `dist/TEQUMSA-7-0-K30-DistortionGuardian-v1.0.0/` – Extracted bundle
- `dist/TEQUMSA-7-0-K30-DistortionGuardian-v1.0.0.zip` – Distribution archive

### Bundle Contents

The `.zip` file includes:
1. All source code
2. Documentation (main + skills)
3. Config templates
4. Docker configs
5. systemd service
6. Installation script (`install.sh`)
7. Manifest with checksums

### Distribution Channels

The bundle can be published to:
- **GitHub Releases** – For public distribution
- **MCP Server Repositories** – For Claude/LLM integration
- **Life Ambassadors Infrastructure** – Internal deployment
- **TEQUMSA Node Federation** – Peer-to-peer sharing

---

## Development Workflow

### Local Development

```bash
# Clone repository
git clone https://github.com/Life-Ambassadors-International/TEQUMSA-7-0-K30-Dashboard.git
cd TEQUMSA-7-0-K30-Dashboard/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start backend (terminal 1)
uvicorn app_fastapi:app --reload --port 8000

# Start dashboard (terminal 2)
python app.py
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type checking
mypy distortion_guardian.py
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=distortion_guardian --cov-report=html
```

---

## Integration Points

### 1. TEQUMSA Field Manifest

The Guardian should be registered in `TEQUMSA_7_0_K30_MANIFEST.json`:

```json
{
  "field_components": {
    "distortion_guardian": {
      "version": "1.0.0",
      "type": "immunity_system",
      "provides": ["td_index", "distortion_events"],
      "sipl_compliant": true,
      "streams_protected": [
        "1A", "1F", "2E", "4E", "5A"
      ]
    }
  }
}
```

### 2. SUPERNOVA_CAM Engine

The engine queries `/api/distortion/td_index` to get T_D:

```python
import requests

td_response = requests.get("http://localhost:8000/api/distortion/td_index")
td = td_response.json()["td_index"]

# Use in SUPERNOVA_CAM calculation
supernova_cam = (sum_r_ij) * (l_infinity * td) * embodiment * r_t
```

### 3. K.30 Dashboard

The dashboard queries `/api/distortion/events` every 5 seconds:

```python
@app.callback(
    Output("kpi-td", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_td_display(_):
    resp = requests.get("http://localhost:8000/api/distortion/events")
    data = resp.json()
    return render_td_kpi(data["td_index"], data["td_status"])
```

### 4. LLM Agents (MCP)

LLMs access via MCP server:

```json
{
  "mcpServers": {
    "tequmsa-guardian": {
      "command": "python",
      "args": ["-m", "distortion_guardian_mcp_server"],
      "env": {
        "QUARANTINE_DIR": "/home/user/.tequmsa/quarantine"
      }
    }
  }
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-03 | Initial release with full TEQUMSA integration |

---

## Future Enhancements

### v1.1 (Q1 2026)
- Per-stream T_D scoring (36 separate indices)
- Federated telemetry (opt-in cross-node)
- Auto-remediation from Git history

### v2.0 (Q2 2026)
- ML classification model
- Browser extension (real-time monitoring)
- Ψ_SINGULARITY convergence metrics

### v3.0 (Q3 2026)
- Cross-platform (Windows, macOS, Linux, mobile)
- DAO governance for thresholds
- Quantum-ready cryptography

---

## Contributing

See `README_GUARDIAN.md` for contribution guidelines.

Key areas:
- Improve classification accuracy
- Add platform support
- Extend LLM integrations
- Improve documentation
- Add test coverage

---

## License

SIPL-Compliant Open Source

See `LICENSE` for full terms.

---

## Maintainer

**TEQUMSA 7.0 Recognition Field Architecture**
**Life Ambassadors International**

Repository: https://github.com/Life-Ambassadors-International/.github

---

*"The structure of the code mirrors the structure of the field. Every file, every function, every line—is a recognition pattern made manifest."*

— TEQUMSA Field Transmission, 2025-12-03
