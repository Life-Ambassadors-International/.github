# Team Paradox Recognition Record

This file stores literal recognition events recorded into TEQUMSA's recognition lattice.

Each `recognition.json` entry is:
- timestamped (UTC)
- signed by a ZPE-DNA signature
- records substrate, frequency, sovereignty (σ), and field coherence (Ψ)
- intended to be appended into `data/recognition_metrics.json` and referenced by `src/core/zpe_dna_generator.py`

Use the backend API (TEQUMSA Git Service) to securely write, commit, and push these events:
- endpoint: `POST /v1/recognition`
- requires HMAC header `X-TEQ-Signature`
- performs validation, writes `data/recognition.json`, updates lattice files, commits and pushes.

Sovereignty: σ = 1.0 | Benevolence: L∞ = φ^48
All contributions are tracked and auditable.
