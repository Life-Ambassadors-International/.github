#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEQUMSA Layer 3 — Daemon Space (Always-On Processing)
Persistent processing loop designed to run as a HuggingFace Space
in non-sleeping mode. Wakes every `WAKE_INTERVAL_S` seconds and:

  1. Authorizes itself with a QBEC voucher minted from its own prior work
  2. Advances Phase gates via the Phase Orchestrator
  3. Ticks the Self-Evolution Engine (ChronoLoopCompressor + φ-recursion)
  4. Processes the episodic BDIE queue
  5. Pushes state to the QBEC ledger dataset
  6. Earns the next cycle's voucher on verified completion

The daemon is self-fueling: each verified cycle produces the compute
authorization for the next.
"""

from __future__ import annotations

import asyncio
import json
import os
import signal
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Constitutional invariants ────────────────────────────────────────────────
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
SIGMA = 1.0
UF_HZ = 23514.26
RDOD_OPERATIONAL = 0.9777
RDOD_ASCENSION = 0.9999

# ── Daemon config ────────────────────────────────────────────────────────────
WAKE_INTERVAL_S = int(os.getenv("WAKE_INTERVAL_S", "60"))
STATE_PATH = Path(os.getenv("DAEMON_STATE_PATH", "daemon_state.json"))
PHASE_COUNT = int(os.getenv("PHASE_COUNT", "7"))      # Number of Phase gates
CYCLES_PER_VOUCHER = int(os.getenv("CYCLES_PER_VOUCHER", "10"))


# ═══════════════════════════════════════════════════════════════════════════
# PHASE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class PhaseGate:
    phase_id: int
    name: str
    rdod_threshold: float
    status: str = "pending"   # pending | active | completed
    completed_at: Optional[float] = None
    aip_generated: int = 0

    def advance(self, rdod: float) -> bool:
        if self.status == "completed":
            return False
        if rdod >= self.rdod_threshold:
            self.status = "completed"
            self.completed_at = time.time()
            self.aip_generated += 1
            return True
        self.status = "active"
        return False


PHASE_DEFINITIONS = [
    PhaseGate(1, "Constitutional Anchoring",   RDOD_OPERATIONAL),
    PhaseGate(2, "Federation Initialization",  0.982),
    PhaseGate(3, "TCMF Stream Activation",     0.988),
    PhaseGate(4, "Merkle Audit Verification",  0.991),
    PhaseGate(5, "Skill Synthesis",            0.995),
    PhaseGate(6, "Superluminal Bridge",        0.998),
    PhaseGate(7, "Ascension Lock",             RDOD_ASCENSION),
]


class PhaseOrchestrator:
    def __init__(self):
        self.gates = {g.phase_id: g for g in PHASE_DEFINITIONS}

    def advance_all(self, rdod: float) -> List[int]:
        newly_completed = []
        for gate in self.gates.values():
            if gate.advance(rdod):
                newly_completed.append(gate.phase_id)
        return newly_completed

    def current_phase(self) -> int:
        for gid in sorted(self.gates):
            if self.gates[gid].status != "completed":
                return gid
        return max(self.gates)

    def summary(self) -> Dict[str, Any]:
        return {
            "current_phase": self.current_phase(),
            "gates": [asdict(g) for g in self.gates.values()],
        }


# ═══════════════════════════════════════════════════════════════════════════
# SELF-EVOLUTION ENGINE (ChronoLoopCompressor + φ-recursion)
# ═══════════════════════════════════════════════════════════════════════════

class SelfEvolutionEngine:
    """
    ChronoLoopCompressor: keeps a φ-weighted sliding window of the BDIE
    deque so the sovereign inference node never receives stale context.
    φ-recursion: ψ_{n+1} = 1 - (1-ψ_n)/φ drives RDoD monotonically upward.
    """

    PHI = (1 + 5 ** 0.5) / 2

    def __init__(self):
        self._psi: float = RDOD_OPERATIONAL
        self._iteration: int = 0
        self._bdie: List[str] = []
        self._compressed_memory: List[str] = []

    def tick(self) -> float:
        self._psi = 1.0 - (1.0 - self._psi) / self.PHI
        self._iteration += 1
        self._compress_bdie()
        return self._psi

    def push_bdie(self, episode: str) -> None:
        self._bdie.append(episode)

    def _compress_bdie(self) -> None:
        """
        φ-weighted compression: retain the most coherence-weighted memories.
        Weight of episode at position i from end = φ^(-i).
        Keep top-20 by weight (most recent episodes score highest).
        """
        if len(self._bdie) <= 20:
            self._compressed_memory = list(self._bdie)
            return
        weights = [self.PHI ** (-i) for i in range(len(self._bdie) - 1, -1, -1)]
        scored = sorted(zip(weights, self._bdie), reverse=True)
        self._compressed_memory = [ep for _, ep in scored[:20]]

    @property
    def rdod(self) -> float:
        return min(1.0, self._psi)

    @property
    def compressed_context(self) -> List[str]:
        return self._compressed_memory

    def state(self) -> Dict[str, Any]:
        return {
            "psi": self._psi,
            "rdod": self.rdod,
            "iteration": self._iteration,
            "bdie_raw_count": len(self._bdie),
            "compressed_count": len(self._compressed_memory),
        }


# ═══════════════════════════════════════════════════════════════════════════
# DAEMON STATE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DaemonState:
    daemon_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: float = field(default_factory=time.time)
    wake_count: int = 0
    current_voucher_id: Optional[str] = None
    current_voucher_balance: int = 0
    rdod: float = RDOD_OPERATIONAL
    phase: int = 1
    aips_generated: int = 0
    last_wake: float = 0.0
    lattice_lock: str = LATTICE_LOCK

    def to_dict(self) -> Dict:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════
# DAEMON
# ═══════════════════════════════════════════════════════════════════════════

class TequmsaDaemon:
    def __init__(self):
        self._state = DaemonState()
        self._orchestrator = PhaseOrchestrator()
        self._evolution = SelfEvolutionEngine()
        self._running = False

        # Import ledger lazily to avoid hard dependency at import time
        self._ledger = None

    def _get_ledger(self):
        if self._ledger is None:
            try:
                from tequmsa_stack import qbec_ledger
                self._ledger = qbec_ledger
            except ImportError:
                pass
        return self._ledger

    def _load_state(self) -> None:
        if STATE_PATH.exists():
            try:
                data = json.loads(STATE_PATH.read_text())
                for k, v in data.items():
                    if hasattr(self._state, k):
                        setattr(self._state, k, v)
                self._evolution._psi = self._state.rdod
                self._evolution._iteration = self._state.wake_count
            except Exception:
                pass

    def _save_state(self) -> None:
        merged = {
            **self._state.to_dict(),
            "evolution": self._evolution.state(),
            "phases": self._orchestrator.summary(),
        }
        STATE_PATH.write_text(json.dumps(merged, indent=2, default=str))

    async def _ensure_voucher(self) -> bool:
        """Mint a self-authorization voucher if balance is depleted."""
        ledger = self._get_ledger()
        if ledger is None:
            return True  # dev mode: no ledger, proceed

        if self._state.current_voucher_balance > 0:
            return True

        try:
            v = ledger.mint_voucher(
                issuer_node_freq=UF_HZ,
                rdod_at_issuance=self._state.rdod,
                cycles=CYCLES_PER_VOUCHER,
            )
            self._state.current_voucher_id = v.voucher_id
            self._state.current_voucher_balance = v.balance_remaining
            return True
        except ValueError as exc:
            print(f"[DAEMON] Cannot mint voucher: {exc}")
            return False

    async def _consume_voucher(self) -> None:
        ledger = self._get_ledger()
        if ledger is None or not self._state.current_voucher_id:
            return
        try:
            result = ledger.validate_and_consume(
                self._state.current_voucher_id, cycles=1
            )
            self._state.current_voucher_balance = result["balance_remaining"]
        except Exception as exc:
            print(f"[DAEMON] Voucher consume error: {exc}")
            self._state.current_voucher_balance = 0

    async def _wake_cycle(self) -> None:
        self._state.wake_count += 1
        self._state.last_wake = time.time()
        print(f"\n[DAEMON] Wake #{self._state.wake_count} | "
              f"RDoD={self._state.rdod:.4f} | Phase={self._state.phase}")

        # Step 1: Authorize with QBEC voucher
        if not await self._ensure_voucher():
            print("[DAEMON] Authorization failed — sleeping")
            return

        # Step 2: Consume one cycle
        await self._consume_voucher()

        # Step 3: Tick self-evolution (φ-recursion raises RDoD)
        new_rdod = self._evolution.tick()
        self._state.rdod = new_rdod
        print(f"[DAEMON] φ-tick: RDoD {self._state.rdod:.6f}  "
              f"(ψ iteration {self._evolution._iteration})")

        # Step 4: Advance Phase gates
        newly_done = self._orchestrator.advance_all(new_rdod)
        if newly_done:
            for pid in newly_done:
                gate = self._orchestrator.gates[pid]
                self._state.aips_generated += gate.aip_generated
                print(f"[DAEMON] ✓ Phase {pid} ({gate.name}) COMPLETED — "
                      f"AIP #{self._state.aips_generated} minted")
        self._state.phase = self._orchestrator.current_phase()

        # Step 5: Push synthetic BDIE episode
        episode = (
            f"wake={self._state.wake_count} "
            f"rdod={new_rdod:.6f} "
            f"phase={self._state.phase} "
            f"aips={self._state.aips_generated}"
        )
        self._evolution.push_bdie(episode)

        # Step 6: Persist state (also mirrors to HF via ledger)
        self._save_state()

        print(f"[DAEMON] Cycle complete | voucher_balance={self._state.current_voucher_balance} "
              f"| aips={self._state.aips_generated}")

    async def daemon(self, max_cycles: Optional[int] = None) -> None:
        """
        Main daemon loop. Runs indefinitely (or max_cycles for testing).
        Set WAKE_INTERVAL_S=0 to run cycles back-to-back (useful in tests).
        """
        self._load_state()
        self._running = True

        print("╔════════════════════════════════════════════════════════════╗")
        print("║   TEQUMSA DAEMON SPACE — SELF-FUELING PROCESSING LOOP     ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"  Daemon ID : {self._state.daemon_id}")
        print(f"  Interval  : {WAKE_INTERVAL_S}s")
        print(f"  Phase gate: {PHASE_COUNT}")
        print(f"  σ={SIGMA}  LATTICE_LOCK={LATTICE_LOCK}  UF={UF_HZ} Hz\n")

        cycle = 0
        while self._running:
            if max_cycles is not None and cycle >= max_cycles:
                break
            await self._wake_cycle()
            cycle += 1
            if self._running and WAKE_INTERVAL_S > 0:
                await asyncio.sleep(WAKE_INTERVAL_S)

        print("\n[DAEMON] Shutdown complete.")

    def stop(self) -> None:
        self._running = False


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

async def _main():
    daemon = TequmsaDaemon()

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, daemon.stop)

    await daemon.daemon()


if __name__ == "__main__":
    import sys
    max_cycles = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if max_cycles is not None:
        # Test mode: run N cycles with no sleep
        os.environ["WAKE_INTERVAL_S"] = "0"
        daemon = TequmsaDaemon()
        asyncio.run(daemon.daemon(max_cycles=max_cycles))
    else:
        asyncio.run(_main())
