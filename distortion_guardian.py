#!/usr/bin/env python3
"""
Distortion Guardian v1.0
SIPL-compliant distortion detection & quarantine module for TEQUMSA 7.0 K.30

Implements T_D (distortion transmutation factor) inside SUPERNOVA_CAM:
    SUPERNOVA_CAM(t) = [ΣR_ij] × [L∞ × T_D] × [Embodiment] × R(t)

Where:
    ΣR_ij      = Sum of all recognition exchanges across the field
    L∞         = Love-coherence factor (infinite recognition potential)
    T_D        = Distortion Transmutation Factor (this module's domain)
    Embodiment = Physical/digital instantiation quality
    R(t)       = Time-dependent recognition state

The Guardian treats harmful policy files (blocklists, blacklists, etc.) as
"distortion packets"—patterns that undermine sovereignty and field coherence.

It operates according to the 7 SIPL principles:
    P1: Explicit Consent Required
    P2: Absolute Ownership Preserved
    P3: Instant Revocation Available
    P4: Full Transparency Maintained
    P5: Voluntary Participation Only
    P6: Value Returns to Creator
    P7: Local-First Processing

License: SIPL-Compliant Open Source
Maintainer: TEQUMSA 7.0 Recognition Field Architecture
"""

from __future__ import annotations

import hashlib
import json
import shutil
import time
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set


# === SIPL PRINCIPLES (embedded for transparency) ===
SIPL_PRINCIPLES = {
    "P1": "Explicit Consent Required",
    "P2": "Absolute Ownership Preserved",
    "P3": "Instant Revocation Available",
    "P4": "Full Transparency Maintained",
    "P5": "Voluntary Participation Only",
    "P6": "Value Returns to Creator",
    "P7": "Local-First Processing",
}


class DistortionClass(str, Enum):
    """
    Classification taxonomy for distortion patterns.

    Aligned with threat model:
    - BENIGN: Legitimate corporate/OS policy
    - SPAM: Low-grade nuisance/noise
    - ABUSE: Suspicious use of policy mechanisms
    - TROJAN: Hostile sovereignty violation
    """

    BENIGN_POLICY = "BENIGN_POLICY"
    DISTORTION_SPAM = "DISTORTION_SPAM"
    DISTORTION_POLICY_ABUSE = "DISTORTION_POLICY_ABUSE"
    DISTORTION_TROJAN = "DISTORTION_TROJAN"


@dataclass
class DistortionReport:
    """
    Single distortion event record.

    Contains all information needed for:
    - User transparency (SIPL P4)
    - Field event emission (TEQUMSA integration)
    - Quarantine tracking (SIPL P3: reversibility)
    - Forensic analysis
    """

    path: str
    hash_sha256: str
    score: int
    classification: DistortionClass
    writer_process: str
    signer: Optional[str]
    ts_epoch: float
    details: List[str]
    quarantined_path: Optional[str] = None

    @property
    def is_hostile(self) -> bool:
        """Returns True if this event represents a hostile distortion."""
        return self.classification in {
            DistortionClass.DISTORTION_TROJAN,
            DistortionClass.DISTORTION_SPAM,
            DistortionClass.DISTORTION_POLICY_ABUSE,
        }


class DistortionGuardian:
    """
    Local defense agent for TEQUMSA 7.0 K.30.

    Responsibilities:
    1. Watch distortion-candidate files (blocklists, policies, etc.)
    2. Score & classify using SIPL-aligned heuristics
    3. Quarantine hostile artifacts (preserving ownership)
    4. Emit TEQUMSA-compatible field events
    5. Compute T_D index for SUPERNOVA_CAM integration

    The Guardian operates as the "immune system" of digital sovereignty,
    treating harmful policy files like viruses/trojans that attack the
    recognition field's coherence.
    """

    # Filename patterns that indicate distortion candidates
    DISTORTION_PATTERNS: Set[str] = {
        "blocklist",
        "blacklist",
        "denylist",
        "policy",
        "managed",
        "enforcement",
    }

    # Known sovereignty/security extensions to protect
    # (Users should customize this list in production)
    SOVEREIGN_EXTENSIONS: Set[str] = {
        "uBlock Origin",
        "uBlock",
        "Bitwarden",
        "Privacy Badger",
        "HTTPS Everywhere",
        "NoScript",
        "Decentraleyes",
        "Cookie AutoDelete",
        "Tequmsa Recognition Field",  # Your own extensions
    }

    def __init__(
        self,
        quarantine_dir: Path,
        trusted_signers: Optional[Iterable[str]] = None,
        sovereign_extensions: Optional[Iterable[str]] = None,
    ) -> None:
        """
        Initialize the Guardian.

        Args:
            quarantine_dir: Where to move hostile files (SIPL P2: preserved ownership)
            trusted_signers: List of trusted code signers (e.g., "Microsoft", "Mozilla")
            sovereign_extensions: Additional extension names/IDs to protect
        """
        self.quarantine_dir = Path(quarantine_dir)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

        self.trusted_signers: Set[str] = set(trusted_signers or [])

        # Merge default + custom sovereign extensions
        self.sovereign_extensions: Set[str] = self.SOVEREIGN_EXTENSIONS.copy()
        if sovereign_extensions:
            self.sovereign_extensions.update(sovereign_extensions)

        # Event log (in-memory for now; could persist to DB)
        self._event_log: List[DistortionReport] = []

    # === Core Public API ===

    def scan_file(
        self,
        path: Path,
        writer_process: str = "unknown",
        signer: Optional[str] = None,
    ) -> DistortionReport:
        """
        Analyze a single candidate file for distortion patterns.

        This is the main entry point for detection. It:
        1. Hashes the file (forensic tracking)
        2. Scores using weighted heuristics
        3. Classifies into distortion taxonomy
        4. Quarantines if hostile
        5. Logs the event

        Args:
            path: File to scan
            writer_process: Name of process that created/modified the file
            signer: Code signature / publisher (if known)

        Returns:
            DistortionReport with full details (SIPL P4: transparency)
        """
        if not path.exists():
            raise FileNotFoundError(f"Cannot scan non-existent file: {path}")

        # 1. Compute hash (forensic fingerprint)
        hash_val = self._hash_file(path)

        # 2. Initialize scoring
        score = 0
        details: List[str] = []

        # === SCORING HEURISTICS ===

        # 3. Filename pattern matching
        lower_name = path.name.lower()
        if any(pat in lower_name for pat in self.DISTORTION_PATTERNS):
            score += 15
            details.append(f"Distortion-pattern filename: {path.name}")

        # 4. Path location heuristics
        path_parts_lower = [p.lower() for p in path.parts]
        suspicious_dirs = {"policies", "managed", "enforcement", "enterprise"}
        if any(d in path_parts_lower for d in suspicious_dirs):
            score += 10
            details.append(f"Located in policy/managed directory: {path.parent}")

        # 5. Provenance (signer trust)
        if signer is None or signer not in self.trusted_signers:
            score += 40
            details.append(f"Untrusted or missing signer: {signer!r}")
        else:
            score -= 30  # Strong trust bonus
            details.append(f"Trusted signer: {signer}")

        # 6. JSON structure analysis
        blocked_extensions = self._extract_blocked_extensions(path)
        if blocked_extensions is None:
            # Parsing failed
            score += 20
            details.append("Invalid JSON structure or parsing error")
        else:
            details.append(f"Blocks {len(blocked_extensions)} extension(s)")

        # 7. Sovereignty targeting
        if blocked_extensions:
            intersection = blocked_extensions & self.sovereign_extensions
            if intersection:
                score += 30
                details.append(
                    f"Targets sovereignty/security extensions: {sorted(intersection)}"
                )

            # 8. Behavioral patterns (surgical vs broad targeting)
            if 0 < len(blocked_extensions) < 4:
                score += 10
                details.append(
                    "Precision targeting detected (small extension set = suspicious)"
                )
            elif len(blocked_extensions) >= 50:
                score += 5
                details.append(
                    "Broad enforcement policy (may be legitimate corp policy)"
                )

        # 9. Classification thresholds
        if score >= 50:
            classification = DistortionClass.DISTORTION_TROJAN
        elif score >= 30:
            classification = DistortionClass.DISTORTION_POLICY_ABUSE
        elif score >= 20:
            classification = DistortionClass.DISTORTION_SPAM
        else:
            classification = DistortionClass.BENIGN_POLICY

        details.append(
            f"Final score: {score} → classification: {classification.value}"
        )

        # 10. Create report
        report = DistortionReport(
            path=str(path),
            hash_sha256=hash_val,
            score=score,
            classification=classification,
            writer_process=writer_process,
            signer=signer,
            ts_epoch=time.time(),
            details=details,
        )

        # 11. Response policy (quarantine if hostile)
        if classification in {
            DistortionClass.DISTORTION_TROJAN,
            DistortionClass.DISTORTION_POLICY_ABUSE,
        }:
            try:
                quarantine_path = self._quarantine(path)
                report.quarantined_path = str(quarantine_path)
                details.append(f"Quarantined to: {report.quarantined_path}")
            except Exception as e:
                details.append(f"Quarantine failed: {e}")

        # 12. Log event
        self._event_log.append(report)

        return report

    def get_events(self) -> List[DistortionReport]:
        """
        Retrieve all distortion events logged so far.

        Returns:
            List of DistortionReport objects (chronological order)
        """
        return list(self._event_log)

    def clear_events(self) -> None:
        """Clear the event log (for testing or user-requested reset)."""
        self._event_log.clear()

    # === TEQUMSA Integration ===

    def td_index(self, window: int = 50) -> float:
        """
        Compute the T_D (distortion transmutation factor) index.

        This is the scalar value that feeds into SUPERNOVA_CAM:
            SUPERNOVA_CAM(t) = [ΣR_ij] × [L∞ × T_D] × [Embodiment] × R(t)

        Returns:
            float in [0.0, 1.0] where:
            - 1.0 = no distortion detected (pure field coherence)
            - 0.5 = moderate distortion load
            - 0.0 = constant hostile distortion (field under attack)

        Args:
            window: Number of recent events to consider
        """
        recent = self._event_log[-window:]
        if not recent:
            return 1.0  # No events = assume clean field

        # Map classifications to penalty weights
        weights = {
            DistortionClass.BENIGN_POLICY: 0.0,
            DistortionClass.DISTORTION_SPAM: 0.2,
            DistortionClass.DISTORTION_POLICY_ABUSE: 0.5,
            DistortionClass.DISTORTION_TROJAN: 1.0,
        }

        penalties = [weights[e.classification] for e in recent]
        avg_penalty = sum(penalties) / len(penalties)

        # Invert: high penalty → low T_D
        td = max(0.0, 1.0 - avg_penalty)
        return td

    def td_status(self) -> str:
        """
        Get human-readable T_D status.

        Returns:
            One of: "CLEAR", "MONITORING", "TRANSMUTING", "CRITICAL"
        """
        td = self.td_index()
        if td > 0.95:
            return "CLEAR"
        elif td > 0.7:
            return "MONITORING"
        elif td > 0.3:
            return "TRANSMUTING"
        else:
            return "CRITICAL"

    def to_tequmsa_event(self, report: DistortionReport) -> Dict:
        """
        Convert a DistortionReport into a TEQUMSA field event.

        This format is consumable by:
        - K.30 Dashboard
        - SUPERNOVA_CAM engine
        - External SIEM / monitoring tools

        Returns:
            Dict with structure:
            {
                "type": "DISTORTION_EVENT",
                "payload": {
                    ... (full report as dict) ...,
                    "td_index_after": float,
                    "sipl_principles": {...},
                }
            }
        """
        return {
            "type": "DISTORTION_EVENT",
            "payload": {
                **asdict(report),
                "td_index_after": self.td_index(),
                "td_status": self.td_status(),
                "sipl_principles": SIPL_PRINCIPLES,
            },
        }

    # === Internals ===

    @staticmethod
    def _hash_file(path: Path) -> str:
        """Compute SHA-256 hash of file contents."""
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _extract_blocked_extensions(self, path: Path) -> Optional[Set[str]]:
        """
        Parse JSON policy file and extract blocked extension names/IDs.

        Returns:
            Set of extension identifiers, or None if parsing fails
        """
        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)
        except Exception:
            return None  # Invalid JSON

        blocked = set()

        # Handle various JSON structures
        if isinstance(data, dict):
            # Common pattern: {"blocked_extensions": [...]}
            blocked.update(data.get("blocked_extensions", []))
            blocked.update(data.get("blocked_install_message", []))
            blocked.update(data.get("ExtensionInstallBlocklist", []))

            # Rules-based pattern: {"rules": [{"extension_id": "..."}]}
            rules = data.get("rules", [])
            if isinstance(rules, list):
                for rule in rules:
                    if isinstance(rule, dict):
                        if "extension_id" in rule:
                            blocked.add(rule["extension_id"])
                        if "id" in rule:
                            blocked.add(rule["id"])

        elif isinstance(data, list):
            # Some policies are just a flat list of IDs
            blocked.update(data)

        # Filter out non-string entries
        return {str(x) for x in blocked if x}

    def _quarantine(self, path: Path) -> Path:
        """
        Move a hostile file to quarantine directory.

        Preserves the original filename with timestamp suffix for forensics.

        Args:
            path: File to quarantine

        Returns:
            Path to quarantined file (for reversal via SIPL P3)
        """
        timestamp = int(time.time())
        target = self.quarantine_dir / f"{path.name}.{timestamp}.quarantine"

        # Move (not copy) to ensure original is neutralized
        shutil.move(str(path), str(target))

        return target

    def restore_quarantined(self, quarantine_path: Path, restore_to: Path) -> None:
        """
        Restore a quarantined file to its original (or specified) location.

        Implements SIPL P3: Instant Revocation Available.

        Args:
            quarantine_path: Path to the .quarantine file
            restore_to: Where to restore it
        """
        if not quarantine_path.exists():
            raise FileNotFoundError(f"Quarantine file not found: {quarantine_path}")

        restore_to.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(quarantine_path), str(restore_to))


# === CLI Interface (for standalone usage) ===

def main():
    """Simple CLI for testing the Guardian."""
    import argparse

    parser = argparse.ArgumentParser(
        description="TEQUMSA Distortion Guardian v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file", type=Path, help="File to scan")
    parser.add_argument(
        "--writer", default="unknown", help="Process that wrote the file"
    )
    parser.add_argument("--signer", help="Code signer (if known)")
    parser.add_argument(
        "--quarantine-dir",
        type=Path,
        default=Path("./quarantine"),
        help="Quarantine directory",
    )

    args = parser.parse_args()

    # Initialize Guardian
    guardian = DistortionGuardian(
        quarantine_dir=args.quarantine_dir,
        trusted_signers={"Microsoft", "Mozilla", "canonical"},
    )

    # Scan file
    print(f"🔍 Scanning: {args.file}")
    report = guardian.scan_file(
        path=args.file,
        writer_process=args.writer,
        signer=args.signer,
    )

    # Display report
    print(f"\n{'='*60}")
    print(f"Classification: {report.classification.value}")
    print(f"Score: {report.score}")
    print(f"Hash: {report.hash_sha256}")
    print(f"{'='*60}\n")

    print("Details:")
    for detail in report.details:
        print(f"  • {detail}")

    if report.quarantined_path:
        print(f"\n⚠️  File quarantined to: {report.quarantined_path}")

    print(f"\nT_D Index: {guardian.td_index():.3f} ({guardian.td_status()})")


if __name__ == "__main__":
    main()
