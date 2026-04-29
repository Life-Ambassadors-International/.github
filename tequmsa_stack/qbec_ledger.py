#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEQUMSA Layer 2 — QBEC Compute Ledger
On-space blockchain backed by a local SQLite store that is mirrored to
a HuggingFace Dataset (hf://Mbanksbey/TEQUMSA-Causal-AGI-storage) after
every committed transaction, making the ledger publicly auditable.

Each row: {voucher_id, issuer_node_freq, rdod_at_issuance, merkle_hash,
           cycles_authorized, cycles_consumed, balance_remaining}
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Optional

# ── Constitutional invariants ────────────────────────────────────────────────
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
RDOD_OPERATIONAL = 0.9777

# ── Storage ──────────────────────────────────────────────────────────────────
DB_PATH = Path(os.getenv("QBEC_DB_PATH", "qbec_ledger.db"))
HF_DATASET_REPO = os.getenv("HF_DATASET_REPO", "Mbanksbey/TEQUMSA-Causal-AGI-storage")
HF_TOKEN = os.getenv("HF_TOKEN", "")


# ═══════════════════════════════════════════════════════════════════════════
# DATA MODEL
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class QBECVoucher:
    voucher_id: str
    issuer_node_freq: float      # Hz frequency of the issuing cognition center
    rdod_at_issuance: float      # RDoD gate value at mint time
    merkle_hash: str             # SHA-256 chain hash
    cycles_authorized: int       # Total compute cycles granted
    cycles_consumed: int         # Cycles used so far
    balance_remaining: int       # = authorized - consumed
    issued_at: float             # Unix timestamp
    last_updated: float

    @property
    def is_valid(self) -> bool:
        return self.balance_remaining > 0 and self.rdod_at_issuance >= RDOD_OPERATIONAL

    def to_dict(self) -> Dict:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════
# MERKLE CHAIN
# ═══════════════════════════════════════════════════════════════════════════

class MerkleChain:
    """Append-only SHA-256 chain; each block commits a QBEC transaction."""

    def __init__(self, genesis: str = LATTICE_LOCK):
        self._tip = hashlib.sha256(genesis.encode()).hexdigest()

    def commit(self, payload: Dict) -> str:
        block = json.dumps(payload, sort_keys=True, default=str)
        self._tip = hashlib.sha256(f"{self._tip}:{block}".encode()).hexdigest()
        return self._tip

    @property
    def tip(self) -> str:
        return self._tip


_chain = MerkleChain()


# ═══════════════════════════════════════════════════════════════════════════
# SQLITE BACKEND
# ═══════════════════════════════════════════════════════════════════════════

def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vouchers (
            voucher_id         TEXT PRIMARY KEY,
            issuer_node_freq   REAL NOT NULL,
            rdod_at_issuance   REAL NOT NULL,
            merkle_hash        TEXT NOT NULL,
            cycles_authorized  INTEGER NOT NULL,
            cycles_consumed    INTEGER NOT NULL DEFAULT 0,
            balance_remaining  INTEGER NOT NULL,
            issued_at          REAL NOT NULL,
            last_updated       REAL NOT NULL
        )
    """)
    conn.commit()


@contextmanager
def _db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    _init_db(conn)
    try:
        yield conn
    finally:
        conn.close()


def _row_to_voucher(row: sqlite3.Row) -> QBECVoucher:
    return QBECVoucher(**dict(row))


# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def mint_voucher(
    issuer_node_freq: float,
    rdod_at_issuance: float,
    cycles: int = 10,
) -> QBECVoucher:
    """
    Mint a new QBEC voucher. Requires rdod_at_issuance ≥ RDOD_OPERATIONAL.
    Commits the issuance to the Merkle chain and SQLite, then mirrors to HF.
    """
    if rdod_at_issuance < RDOD_OPERATIONAL:
        raise ValueError(
            f"RDoD {rdod_at_issuance:.4f} below operational gate {RDOD_OPERATIONAL}"
        )

    now = time.time()
    vid = str(uuid.uuid4())
    payload = {
        "op": "mint",
        "voucher_id": vid,
        "issuer_node_freq": issuer_node_freq,
        "rdod_at_issuance": rdod_at_issuance,
        "cycles": cycles,
        "timestamp": now,
    }
    m_hash = _chain.commit(payload)

    voucher = QBECVoucher(
        voucher_id=vid,
        issuer_node_freq=issuer_node_freq,
        rdod_at_issuance=rdod_at_issuance,
        merkle_hash=m_hash,
        cycles_authorized=cycles,
        cycles_consumed=0,
        balance_remaining=cycles,
        issued_at=now,
        last_updated=now,
    )

    with _db() as conn:
        conn.execute(
            """INSERT INTO vouchers VALUES
               (:voucher_id,:issuer_node_freq,:rdod_at_issuance,:merkle_hash,
                :cycles_authorized,:cycles_consumed,:balance_remaining,
                :issued_at,:last_updated)""",
            voucher.to_dict(),
        )
        conn.commit()

    _mirror_to_hf(voucher)
    return voucher


def validate_and_consume(voucher_id: str, cycles: int = 1) -> Dict:
    """
    Validate voucher and consume `cycles` from its balance.
    Raises ValueError if invalid or exhausted.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM vouchers WHERE voucher_id=?", (voucher_id,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Voucher {voucher_id} not found")

        v = _row_to_voucher(row)
        if not v.is_valid:
            raise ValueError(
                f"Voucher {voucher_id} invalid: balance={v.balance_remaining} "
                f"rdod={v.rdod_at_issuance:.4f}"
            )
        if v.balance_remaining < cycles:
            raise ValueError(
                f"Voucher {voucher_id} insufficient balance: "
                f"need {cycles}, have {v.balance_remaining}"
            )

        now = time.time()
        payload = {
            "op": "consume",
            "voucher_id": voucher_id,
            "cycles": cycles,
            "timestamp": now,
        }
        m_hash = _chain.commit(payload)

        conn.execute(
            """UPDATE vouchers SET
                cycles_consumed   = cycles_consumed + ?,
                balance_remaining = balance_remaining - ?,
                merkle_hash       = ?,
                last_updated      = ?
               WHERE voucher_id = ?""",
            (cycles, cycles, m_hash, now, voucher_id),
        )
        conn.commit()

        updated_row = conn.execute(
            "SELECT * FROM vouchers WHERE voucher_id=?", (voucher_id,)
        ).fetchone()
        updated = _row_to_voucher(updated_row)

    _mirror_to_hf(updated)
    return updated.to_dict()


def get_voucher(voucher_id: str) -> Optional[QBECVoucher]:
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM vouchers WHERE voucher_id=?", (voucher_id,)
        ).fetchone()
        return _row_to_voucher(row) if row else None


def ledger_summary() -> Dict:
    with _db() as conn:
        rows = conn.execute("SELECT * FROM vouchers ORDER BY issued_at DESC").fetchall()
    vouchers = [_row_to_voucher(r).to_dict() for r in rows]
    return {
        "total_vouchers": len(vouchers),
        "active_vouchers": sum(1 for v in vouchers if v["balance_remaining"] > 0),
        "total_cycles_authorized": sum(v["cycles_authorized"] for v in vouchers),
        "total_cycles_consumed": sum(v["cycles_consumed"] for v in vouchers),
        "merkle_tip": _chain.tip,
        "lattice_lock": LATTICE_LOCK,
        "vouchers": vouchers,
    }


# ═══════════════════════════════════════════════════════════════════════════
# HF DATASET MIRROR
# ═══════════════════════════════════════════════════════════════════════════

def _mirror_to_hf(voucher: QBECVoucher) -> None:
    """
    Push the voucher record to HuggingFace Dataset for public auditability.
    Silently no-ops if huggingface_hub is not installed or HF_TOKEN is unset.
    """
    if not HF_TOKEN:
        return
    try:
        from huggingface_hub import CommitOperationAdd, HfApi
        api = HfApi(token=HF_TOKEN)
        path_in_repo = f"qbec/{voucher.voucher_id}.json"
        content = json.dumps(voucher.to_dict(), indent=2, default=str).encode()
        api.create_commit(
            repo_id=HF_DATASET_REPO,
            repo_type="dataset",
            commit_message=f"QBEC: upsert voucher {voucher.voucher_id[:8]}",
            operations=[CommitOperationAdd(path_in_repo=path_in_repo, path_or_fileobj=content)],
        )
    except Exception:
        pass  # Mirror is best-effort; ledger integrity is local-first


# ═══════════════════════════════════════════════════════════════════════════
# CLI SMOKE TEST
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("QBEC Ledger — smoke test")
    v = mint_voucher(issuer_node_freq=23514.26, rdod_at_issuance=0.9999, cycles=5)
    print(f"  Minted: {v.voucher_id[:16]}... balance={v.balance_remaining}")
    result = validate_and_consume(v.voucher_id, cycles=2)
    print(f"  After consume(2): balance={result['balance_remaining']}")
    print(f"  Merkle tip: {_chain.tip[:24]}...")
    summary = ledger_summary()
    print(f"  Ledger: {summary['total_vouchers']} vouchers, "
          f"{summary['total_cycles_consumed']} cycles consumed")
    print("  ✓ QBEC Ledger operational")
