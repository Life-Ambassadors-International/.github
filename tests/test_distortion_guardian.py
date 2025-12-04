#!/usr/bin/env python3
"""
Test suite for TEQUMSA Distortion Guardian
Tests classification, scoring, quarantine, and T_D index computation
"""

import json
import tempfile
from pathlib import Path

import pytest

from distortion_guardian import (
    DistortionClass,
    DistortionGuardian,
    DistortionReport,
)


@pytest.fixture
def temp_quarantine():
    """Create temporary quarantine directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def guardian(temp_quarantine):
    """Create Guardian instance with test configuration"""
    return DistortionGuardian(
        quarantine_dir=temp_quarantine,
        trusted_signers={"Microsoft", "Mozilla", "Acme Corporation IT Department"},
        sovereign_extensions={"uBlock Origin", "Bitwarden", "Privacy Badger"},
    )


@pytest.fixture
def fixtures_dir():
    """Get path to test fixtures directory"""
    return Path(__file__).parent / "fixtures"


# === Classification Tests ===


def test_benign_policy_classification(guardian, fixtures_dir):
    """Test that legitimate corporate policy is classified as BENIGN"""
    policy_file = fixtures_dir / "benign_policy.json"

    report = guardian.scan_file(
        path=policy_file,
        writer_process="enterprise_manager",
        signer="Microsoft Corporation",
    )

    assert report.classification == DistortionClass.BENIGN_POLICY
    assert report.score < 20
    assert report.quarantined_path is None  # Should not be quarantined
    assert "Trusted signer" in " ".join(report.details)


def test_hostile_blocklist_classification(guardian, fixtures_dir):
    """Test that hostile blocklist targeting sovereignty extensions is classified as TROJAN"""
    blocklist_file = fixtures_dir / "hostile_blocklist.json"

    report = guardian.scan_file(
        path=blocklist_file,
        writer_process="unknown",
        signer=None,
    )

    assert report.classification == DistortionClass.DISTORTION_TROJAN
    assert report.score >= 50
    assert report.quarantined_path is not None  # Should be quarantined
    assert "Targets sovereignty extensions" in " ".join(report.details)


def test_corp_policy_classification(guardian, fixtures_dir):
    """Test corporate policy with many blocks but trusted signer"""
    policy_file = fixtures_dir / "corp_managed_policy.json"

    report = guardian.scan_file(
        path=policy_file,
        writer_process="group_policy",
        signer="Acme Corporation IT Department",
    )

    # Should be BENIGN because of trusted signer, despite many blocks
    assert report.classification == DistortionClass.BENIGN_POLICY
    assert report.quarantined_path is None
    assert "Trusted signer" in " ".join(report.details)


def test_malformed_json_penalty(guardian, fixtures_dir):
    """Test that malformed JSON receives penalty points"""
    malformed_file = fixtures_dir / "malformed_policy.json"

    report = guardian.scan_file(
        path=malformed_file,
        writer_process="unknown",
        signer=None,
    )

    # Malformed JSON should get penalty points
    assert report.score > 0
    # Check if parsing error was noted in details
    details_text = " ".join(report.details).lower()
    assert "invalid" in details_text or "error" in details_text or "json" in details_text


# === Scoring Tests ===


def test_filename_pattern_scoring(guardian):
    """Test that distortion-pattern filenames receive score penalty"""
    # Create temp file with distortion pattern in name
    with tempfile.NamedTemporaryFile(
        mode="w", suffix="_blocklist.json", delete=False
    ) as f:
        json.dump({"blocked_extensions": []}, f)
        temp_path = Path(f.name)

    try:
        report = guardian.scan_file(temp_path)
        # Should get +15 for filename pattern
        assert report.score >= 15
        assert "filename" in " ".join(report.details).lower()
    finally:
        if temp_path.exists():
            temp_path.unlink()


def test_untrusted_signer_penalty(guardian, fixtures_dir):
    """Test that untrusted/missing signers receive high penalty"""
    policy_file = fixtures_dir / "hostile_blocklist.json"

    report = guardian.scan_file(
        path=policy_file,
        signer=None,  # No signer
    )

    # Untrusted signer should add +40 points
    assert report.score >= 40
    assert "Untrusted" in " ".join(report.details)


def test_trusted_signer_bonus(guardian, fixtures_dir):
    """Test that trusted signers receive score bonus"""
    policy_file = fixtures_dir / "benign_policy.json"

    # Scan with untrusted signer
    report_untrusted = guardian.scan_file(
        path=policy_file,
        signer="RandomCorp",
    )

    # Scan with trusted signer
    report_trusted = guardian.scan_file(
        path=policy_file,
        signer="Microsoft",
    )

    # Trusted version should have significantly lower score (-30 bonus)
    assert report_trusted.score < report_untrusted.score


# === Quarantine Tests ===


def test_quarantine_creation(guardian, fixtures_dir, temp_quarantine):
    """Test that TROJAN files are quarantined"""
    blocklist_file = fixtures_dir / "hostile_blocklist.json"

    # Copy to temp location (don't modify fixture)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(blocklist_file.read_text())
        temp_file = Path(f.name)

    try:
        report = guardian.scan_file(temp_file)

        assert report.quarantined_path is not None
        assert Path(report.quarantined_path).exists()
        assert not temp_file.exists()  # Original should be moved
    finally:
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()


def test_quarantine_restoration(guardian, fixtures_dir, temp_quarantine):
    """Test SIPL P3: Instant Revocation (quarantine restoration)"""
    blocklist_file = fixtures_dir / "hostile_blocklist.json"

    # Copy to temp location
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(blocklist_file.read_text())
        temp_file = Path(f.name)

    original_path = temp_file

    # Scan and quarantine
    report = guardian.scan_file(temp_file)
    quarantine_path = Path(report.quarantined_path)

    assert quarantine_path.exists()
    assert not original_path.exists()

    # Restore
    restore_to = temp_quarantine / "restored.json"
    guardian.restore_quarantined(quarantine_path, restore_to)

    assert restore_to.exists()
    assert not quarantine_path.exists()

    # Cleanup
    if restore_to.exists():
        restore_to.unlink()


# === T_D Index Tests ===


def test_td_index_empty_log(guardian):
    """Test that T_D = 1.0 when no events logged"""
    td = guardian.td_index()
    assert td == 1.0


def test_td_index_all_benign(guardian, fixtures_dir):
    """Test that T_D = 1.0 when all events are BENIGN"""
    policy_file = fixtures_dir / "benign_policy.json"

    # Scan multiple times
    for _ in range(5):
        guardian.scan_file(policy_file, signer="Microsoft")

    td = guardian.td_index()
    assert td == 1.0


def test_td_index_all_trojan(guardian, fixtures_dir):
    """Test that T_D approaches 0.0 when all events are TROJAN"""
    blocklist_file = fixtures_dir / "hostile_blocklist.json"

    # Create multiple temp copies and scan
    for i in range(5):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(blocklist_file.read_text())
            temp_file = Path(f.name)

        try:
            guardian.scan_file(temp_file)
        except:
            pass

    td = guardian.td_index()
    # Should be very low (full penalty for TROJAN = 1.0, so 1.0 - 1.0 = 0.0)
    assert td == 0.0


def test_td_index_mixed_events(guardian, fixtures_dir):
    """Test T_D with mixed event classifications"""
    benign = fixtures_dir / "benign_policy.json"
    hostile = fixtures_dir / "hostile_blocklist.json"

    # Scan benign
    guardian.scan_file(benign, signer="Microsoft")

    # Scan hostile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(hostile.read_text())
        temp_file = Path(f.name)

    try:
        guardian.scan_file(temp_file)
    except:
        pass

    td = guardian.td_index()
    # Should be between 0.0 and 1.0 (mixed penalties)
    assert 0.0 < td < 1.0


# === TEQUMSA Event Format Tests ===


def test_tequmsa_event_format(guardian, fixtures_dir):
    """Test that events are formatted correctly for TEQUMSA field"""
    policy_file = fixtures_dir / "benign_policy.json"

    report = guardian.scan_file(policy_file, signer="Microsoft")
    event = guardian.to_tequmsa_event(report)

    # Check structure
    assert "type" in event
    assert event["type"] == "DISTORTION_EVENT"
    assert "payload" in event

    payload = event["payload"]
    assert "path" in payload
    assert "classification" in payload
    assert "score" in payload
    assert "td_index_after" in payload
    assert "sipl_principles" in payload

    # Check SIPL principles
    sipl = payload["sipl_principles"]
    assert "P1" in sipl
    assert "P2" in sipl
    assert "P3" in sipl
    assert len(sipl) == 7  # All 7 principles


# === T_D Status Tests ===


def test_td_status_clear(guardian, fixtures_dir):
    """Test that T_D status is CLEAR when td > 0.95"""
    policy_file = fixtures_dir / "benign_policy.json"

    # Multiple benign scans
    for _ in range(3):
        guardian.scan_file(policy_file, signer="Microsoft")

    status = guardian.td_status()
    assert status == "CLEAR"


def test_td_status_critical(guardian, fixtures_dir):
    """Test that T_D status is CRITICAL when td <= 0.3"""
    hostile = fixtures_dir / "hostile_blocklist.json"

    # Multiple hostile scans
    for i in range(5):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(hostile.read_text())
            temp_file = Path(f.name)

        try:
            guardian.scan_file(temp_file)
        except:
            pass

    status = guardian.td_status()
    assert status == "CRITICAL"


# === Edge Cases ===


def test_scan_nonexistent_file(guardian):
    """Test that scanning non-existent file raises error"""
    with pytest.raises(FileNotFoundError):
        guardian.scan_file(Path("/nonexistent/file.json"))


def test_empty_file(guardian):
    """Test handling of empty file"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        # Write nothing
        temp_file = Path(f.name)

    try:
        report = guardian.scan_file(temp_file)
        # Should handle gracefully (parse error penalty)
        assert report.score > 0
    finally:
        if temp_file.exists():
            temp_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
