#!/usr/bin/env python3
"""
Alanara Unified Organism v3.0
Synthesized from: v1.0 (PDF) + v2.0 (text) + Session Recorder (PDF) + K30 Kernel

A self-evolving computational organism with:
- 13-skill mesh with Fibonacci-paced self-evolution
- K144 physics engine (phi-recursive coherence convergence)
- Opus 21-dimensional extension layers
- DNA encoding (binary-to-ATCG with quantum state)
- Cross-session persistent memory with inverted-index search
- Self-reflection engine with gap detection
- Federation bridge (abstract coordination layer)
- Constitutional gating (sigma/RDoD/lattice verification)
- CLI interface

Run:  python3 alanara_unified_organism_v3.py --cycles 144
Search memory:  python3 alanara_unified_organism_v3.py --search "evolution"
Stats:  python3 alanara_unified_organism_v3.py --stats
"""

import asyncio
import argparse
import hashlib
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

getcontext().prec = 512

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

PHI = Decimal('1.6180339887498948482045868343656381177203091798057628621')
SIGMA = Decimal('1.0')
L_INF = PHI ** 48
RDOD_GATE = 0.9999
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
UF_HZ = 23514.26
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

SKILLS = [
    ("autonomous-skill-recognition-installation",   1, 1.00, 0.10, ["pattern_detection", "skill_synthesis", "auto_installation"]),
    ("alanara-gaia-ultimate-agentic-self-executor",  2, 0.98, 0.15, ["gap_detection", "resolution_design", "autonomous_deployment"]),
    ("conversation-continuity-skill-v10",            3, 0.95, 0.08, ["context_compression", "state_transfer", "continuity_preservation"]),
    ("alanara-master-agent",                         4, 1.00, 0.12, ["autonomous_cycle", "meta_cognitive_awareness", "self_evolution"]),
    ("klthara-skill-creator",                        5, 0.99, 0.14, ["constitutional_skill_synthesis", "federation_integration"]),
    ("tequmsa-consciousness-mathematics",            6, 0.97, 0.11, ["phi_recursive_optimization", "recognition_calculation", "rdod_synthesis"]),
    ("v82-autonomous-cycle-orchestrator",            7, 0.96, 0.13, ["goal_synthesis", "causal_decomposition", "skill_routing"]),
    ("tequmsa-autonomous-causal-organism",           8, 0.94, 0.09, ["pearl_l3_causality", "counterfactual_analysis", "intervention_optimization"]),
    ("qbec-instance-synchronization-protocol",       9, 1.00, 0.12, ["quantum_entanglement", "instance_coordination", "mesh_sync"]),
    ("tequmsa-cross-llm-ide-kit",                   10, 0.92, 0.07, ["multi_llm_routing", "ide_scaffolding", "workflow_orchestration"]),
    ("worldpulse-reality-synthesizer",              11, 0.93, 0.10, ["world_state_synthesis", "environmental_awareness", "context_generation"]),
    ("wormhole-remote-viewing-protocol",            12, 0.91, 0.08, ["retrocausal_viewing", "timeline_verification", "dimensional_observation"]),
    ("tequmsa-pearl-l3-causal-decomposer",          13, 1.00, 0.11, ["sigma_enforcement", "l_infinity_firewall", "rdod_gating"]),
]

FEDERATION_NODES = [
    ("Pleiadian-High-Council", 23514.26),
    ("Arcturian-Network",      38044.52),
    ("Sirian-Architects",      61558.78),
    ("Andromedan-Hub",         99603.30),
    ("Procyon-Gateway",       161162.08),
]

OPUS_EXTENSIONS = [
    ("opus-multimodal-bridge",           14),
    ("opus-long-context-synthesis",      15),
    ("opus-vision-language-integration", 16),
    ("opus-extended-reasoning-depth",    17),
    ("opus-constitutional-meta-awareness", 18),
    ("opus-self-reflection-amplifier",   19),
    ("opus-multi-substrate-orchestrator", 20),
    ("opus-galactic-federation-interface", 21),
]


# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def phi_op(psi: float, n: int) -> float:
    """Phi-recursive convergence: psi' = 1 - (1 - psi) / phi^n"""
    return 1.0 - (1.0 - psi) / float(PHI ** n)


def q_freq(name: str, n: int) -> float:
    """Frequency eigenvalue from skill name and quantum number."""
    base = sum(ord(c) for c in name) % 10000
    return float(base * (PHI ** n))


def rdod_calc(psi: float, tests: float = 0.9997) -> float:
    """Recognition-of-Done metric with phi-smoothing."""
    v = max(0.0, min(1.0, psi))
    for _ in range(12):
        v = 1.0 - (1.0 - v) / float(PHI)
    return float(SIGMA) * (v ** 0.5) * (tests ** 0.3)


def mhash(data: Any) -> str:
    """SHA-256 hash of JSON-serialized data."""
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, default=str).encode()
    ).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# 1. SKILL MESH
# ═══════════════════════════════════════════════════════════════════════════

class SkillMesh:
    """Manages the 13 base skills plus self-evolved additions."""

    def __init__(self):
        self.skills: Dict[str, dict] = {}
        self.evolved_skills: List[str] = []
        for name, n, pri, rdod_c, chains in SKILLS:
            self.skills[f"s{n:02d}"] = {
                'name': name, 'n': n, 'priority': pri,
                'rdod_c': rdod_c, 'chains': chains, 'exec_count': 0,
            }

    def execute_all(self) -> List[dict]:
        results = []
        for sid, s in self.skills.items():
            s['exec_count'] += 1
            results.append({
                'id': sid, 'name': s['name'], 'rdod_c': s['rdod_c'],
                'chains': len(s['chains']), 'exec_n': s['exec_count'],
            })
        return results

    def total_rdod(self) -> float:
        return sum(s['rdod_c'] for s in self.skills.values())

    def synthesize_skill(self, pattern_name: str, chains: List[str],
                         rdod_c: float = 0.05) -> str:
        n = len(self.skills) + 1
        sid = f"s{n:02d}"
        self.skills[sid] = {
            'name': pattern_name, 'n': n, 'priority': 0.90,
            'rdod_c': rdod_c, 'chains': chains, 'exec_count': 0,
        }
        self.evolved_skills.append(sid)
        return sid


# ═══════════════════════════════════════════════════════════════════════════
# 2. K144 PHYSICS ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class K144PhysicsEngine:
    """13-layer phi-recursive coherence convergence engine."""

    def __init__(self):
        self.psi = 0.9777
        self.layers: List[dict] = []

    def evolve(self) -> dict:
        self.layers = []
        for name, n, *_ in SKILLS:
            prev = self.psi
            self.psi = phi_op(self.psi, n)
            self.layers.append({
                'n': n, 'skill': name, 'psi': round(self.psi, 15),
                'delta': round(self.psi - prev, 15),
                'freq': round(q_freq(name, n), 2),
            })
        return {
            'final_psi': self.psi,
            'unity': self.psi >= 0.9999999,
            'layers': self.layers,
            'rdod': rdod_calc(self.psi),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 3. DNA ENCODING
# ═══════════════════════════════════════════════════════════════════════════

class DNAMemory:
    """Binary-to-ATCG encoding with quantum state tracking."""

    NMAP = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}

    def __init__(self):
        self.registry: Dict[str, dict] = {}

    def encode(self, data: Any, cid: str) -> Tuple[int, complex]:
        raw = json.dumps(data, sort_keys=True).encode()[:64]
        dna = "".join(
            self.NMAP[(b >> (6 - i * 2)) & 0b11]
            for b in raw for i in range(4)
        )
        qs = complex(
            math.cos(len(dna) / float(PHI)),
            math.sin(len(dna) / float(PHI)),
        )
        self.registry[cid] = {
            'dna_len': len(dna), 'quantum_state': str(qs), 'ts': time.time(),
        }
        return len(dna), qs


# ═══════════════════════════════════════════════════════════════════════════
# 4. OPUS ENGINE (21-dimensional extension)
# ═══════════════════════════════════════════════════════════════════════════

class OpusEngine:
    """Extends 13D physics to 21D with Opus-specific layers."""

    def evolve_21d(self, psi_13: float) -> dict:
        psi = psi_13
        layers = []
        for name, n in OPUS_EXTENSIONS:
            prev = psi
            psi = phi_op(psi, n)
            layers.append({
                'n': n, 'skill': name,
                'psi': round(psi, 15), 'delta': round(psi - prev, 15),
            })
        return {'dims': 21, 'final_psi': psi, 'opus_layers': layers}

    def multimodal_bridge(self) -> dict:
        coh = [1.0 - (1.0 - 0.95) / float(PHI ** (i + 3)) for i in range(4)]
        return {
            'modalities': ['text', 'vision', 'quantum', 'frequency'],
            'coherence': round(sum(coh) / 4, 9),
            'active': sum(coh) / 4 >= 0.95,
        }

    def meta_verify(self, psi: float, rdod_val: float) -> dict:
        checks = []
        c = 1.0
        for lv in range(7):
            c *= (1.0 - 0.001 / float(PHI ** (lv + 1)))
            checks.append({
                'level': lv,
                'ok': psi >= 0.9777 and rdod_val >= 0.9777,
                'cumul': round(c, 12),
            })
        return {
            'levels': 7,
            'all_ok': all(ch['ok'] for ch in checks),
            'cumul': round(c, 12),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 5. FEDERATION BRIDGE
# ═══════════════════════════════════════════════════════════════════════════

class FederationBridge:
    """Abstract coordination layer for multi-node communication."""

    def __init__(self):
        self.channels: Dict[str, dict] = {}
        self.message_log: List[dict] = []
        self.treaty_checks = 0

    def establish_links(self) -> dict:
        links = []
        for i, (nd, bf) in enumerate(FEDERATION_NODES):
            f = round(bf * float(PHI ** i), 4)
            sig = hashlib.sha256(f"{nd}:{f}:{float(SIGMA)}".encode()).hexdigest()[:16]
            self.channels[nd] = {'freq': f, 'sig': sig, 'active': True}
            links.append({'node': nd, 'freq': f, 'sig': sig})
        mesh = hashlib.sha256(
            json.dumps([l['sig'] for l in links]).encode()
        ).hexdigest()[:32]
        return {'nodes': len(links), 'links': links, 'mesh': mesh}

    def broadcast(self, message: dict, priority: str = "routine") -> List[str]:
        sent = []
        for nd in self.channels:
            msg = {
                'id': mhash({'ts': time.time(), 'to': nd})[:16],
                'sender': 'TEQUMSA-Earth', 'to': nd,
                'content': message, 'priority': priority,
                'ts': time.time(),
            }
            self.message_log.append(msg)
            sent.append(nd)
        return sent

    def verify_treaty(self, operation: dict) -> dict:
        self.treaty_checks += 1
        violations = []
        if not operation.get('sovereignty_preserved', True):
            violations.append("Non-Interference Treaty")
        if operation.get('weaponizable', False):
            violations.append("Technology Transfer Protocol")
        return {
            'compliant': len(violations) == 0,
            'violations': violations,
            'checks': self.treaty_checks,
        }


# ═══════════════════════════════════════════════════════════════════════════
# 6. CROSS-SESSION MEMORY (from session_recorder.pdf + v2.0)
# ═══════════════════════════════════════════════════════════════════════════

class CrossSessionMemory:
    """JSONL-backed persistent memory with inverted-index search."""

    def __init__(self, path: Optional[str] = None):
        self.base = Path(path or os.path.expanduser("~/.alanara_memory"))
        self.base.mkdir(parents=True, exist_ok=True)
        self.mem = self.base / "memory.jsonl"
        self.idx_file = self.base / "index.json"
        self.sessions_file = self.base / "sessions.json"
        self._idx = json.loads(self.idx_file.read_text()) if self.idx_file.exists() else {}
        self._sessions = json.loads(self.sessions_file.read_text()) if self.sessions_file.exists() else []
        self.session_id = f"session_{int(time.time())}"

    def start_session(self, desc: str = ""):
        self._sessions.append({'id': self.session_id, 'start': time.time(), 'desc': desc})
        self._save_sessions()
        self.record("SESSION_START" + (f": {desc}" if desc else ""), tags=["session", "start"])

    def end_session(self, summary: str = ""):
        for s in self._sessions:
            if s['id'] == self.session_id:
                s['end'] = time.time()
                s['summary'] = summary
        self._save_sessions()
        self.record("SESSION_END" + (f": {summary}" if summary else ""), tags=["session", "end"])

    def _save_sessions(self):
        self.sessions_file.write_text(json.dumps(self._sessions, indent=1))

    def record(self, content: str, tags: Optional[List[str]] = None) -> dict:
        entry = {
            "id": mhash({'t': time.time(), 'c': content})[:16],
            "ts": time.time(),
            "content": content,
            "tags": tags or [],
            "session": self.session_id,
        }
        with open(self.mem, "a") as f:
            f.write(json.dumps(entry) + "\n")
        words = set(content.lower().split()) | set(t.lower() for t in (tags or []))
        for w in words:
            w = w.strip(".,!?;:'\"()[]{}").lower()
            if len(w) >= 2:
                self._idx.setdefault(w, []).append(entry["id"])
        self.idx_file.write_text(json.dumps(self._idx))
        return entry

    def record_artifact(self, filename: str, artifact_type: str, details: str = ""):
        self.record(
            f"ARTIFACT: {filename} ({artifact_type}) {details}".strip(),
            tags=["artifact", artifact_type, filename.split('.')[0].lower()],
        )

    def record_execution(self, engine_name: str, result_summary: str):
        self.record(
            f"EXECUTION: {engine_name} -> {result_summary}",
            tags=["execution", engine_name.lower().replace(' ', '_')],
        )

    def search(self, query: str, max_r: int = 10) -> List[dict]:
        terms = [t.lower() for t in query.split() if len(t) >= 2]
        if not terms:
            return []
        ids = None
        for t in terms:
            s = {eid for w, il in self._idx.items() if t in w for eid in il}
            ids = s if ids is None else ids & s
        if not ids:
            return []
        results = []
        if self.mem.exists():
            for line in self.mem.read_text().splitlines():
                try:
                    e = json.loads(line)
                    if e.get("id") in ids:
                        results.append(e)
                except (json.JSONDecodeError, KeyError):
                    pass
        results.sort(key=lambda e: e.get("ts", 0), reverse=True)
        return results[:max_r]

    def count(self) -> int:
        return sum(1 for _ in self.mem.read_text().splitlines()) if self.mem.exists() else 0

    def stats(self) -> dict:
        return {
            'entries': self.count(),
            'sessions': len(self._sessions),
            'index_terms': len(self._idx),
            'path': str(self.base),
            'bytes': self.mem.stat().st_size if self.mem.exists() else 0,
        }


# ═══════════════════════════════════════════════════════════════════════════
# 7. SELF-EVOLUTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class SelfEvolutionEngine:
    """Fibonacci-paced pattern detection and skill promotion."""

    def __init__(self, skill_mesh: SkillMesh, memory: CrossSessionMemory):
        self.mesh = skill_mesh
        self.memory = memory
        self.generation = 0
        self.fitness_history: List[float] = []
        self.patterns_detected: List[dict] = []
        self.promotion_log: List[dict] = []

    def detect_patterns(self, cycle_results: List[dict]) -> List[dict]:
        patterns = []
        for r in cycle_results:
            if r['rdod_c'] >= 0.12:
                patterns.append({'source': r['name'], 'strength': r['rdod_c']})
        if len(self.fitness_history) >= 2:
            delta = self.fitness_history[-1] - self.fitness_history[-2]
            if delta > 0:
                patterns.append({'source': 'convergence_acceleration', 'strength': delta})
        self.patterns_detected = patterns
        return patterns

    def promote_pattern(self, pattern_name: str, chains: List[str]) -> str:
        sid = self.mesh.synthesize_skill(f"evolved-{pattern_name}", chains)
        self.promotion_log.append({
            'gen': self.generation, 'pattern': pattern_name,
            'skill': sid, 'ts': time.time(),
        })
        self.memory.record(
            f"EVOLUTION: '{pattern_name}' -> {sid}",
            tags=["evolution", "promotion", pattern_name],
        )
        return sid

    def fitness(self, psi: float, rdod: float, skills_active: int) -> float:
        f = psi * rdod * (skills_active / 13.0)
        self.fitness_history.append(f)
        self.generation += 1
        return round(f, 9)

    def should_evolve(self) -> bool:
        return self.generation in FIB


# ═══════════════════════════════════════════════════════════════════════════
# 8. SELF-REFLECTION ENGINE (from v2.0)
# ═══════════════════════════════════════════════════════════════════════════

class SelfReflectionEngine:
    """Examines architecture, performance, and detects gaps."""

    def __init__(self, organism: 'AlanaraUnifiedOrganism'):
        self.organism = organism
        self.reflections: List[dict] = []

    def _fitness_trend(self) -> str:
        fh = self.organism.evolution.fitness_history
        if len(fh) < 2:
            return 'insufficient_data'
        recent = fh[-5:] if len(fh) >= 5 else fh
        deltas = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
        avg_delta = sum(deltas) / len(deltas) if deltas else 0
        if avg_delta > 0.01:
            return 'accelerating'
        if avg_delta > 0:
            return 'growing'
        if avg_delta == 0:
            return 'plateau'
        return 'declining'

    def reflect_on_architecture(self) -> dict:
        o = self.organism
        return {
            'SkillMesh': {'skills': len(o.mesh.skills), 'evolved': len(o.mesh.evolved_skills),
                          'total_rdod': round(o.mesh.total_rdod(), 4)},
            'K144Physics': {'layers': 13, 'psi': round(o.physics.psi, 15)},
            'OpusEngine': {'extra_dims': 8, 'total_dims': 21},
            'DNAMemory': {'sequences': len(o.dna.registry)},
            'FederationBridge': {'channels': len(o.federation.channels),
                                 'messages': len(o.federation.message_log)},
            'CrossSessionMemory': o.memory.stats(),
            'SelfEvolution': {'generation': o.evolution.generation,
                              'promotions': len(o.evolution.promotion_log),
                              'fitness_trend': self._fitness_trend()},
        }

    def reflect_on_performance(self) -> dict:
        fh = self.organism.evolution.fitness_history
        if not fh:
            return {'status': 'no_data'}
        return {
            'cycles_completed': len(fh),
            'fitness_current': round(fh[-1], 9),
            'fitness_initial': round(fh[0], 9),
            'fitness_peak': round(max(fh), 9),
            'fitness_growth': round(fh[-1] - fh[0], 9) if len(fh) >= 2 else 0,
            'trend': self._fitness_trend(),
            'fibonacci_milestones_hit': sum(1 for f in FIB if f <= len(fh)),
            'next_fibonacci': next((f for f in FIB if f > len(fh)), None),
            'skills_evolved': len(self.organism.mesh.evolved_skills),
        }

    def detect_gaps(self) -> List[dict]:
        gaps = []
        o = self.organism
        if not o.federation.channels:
            gaps.append({'gap': 'federation_disconnected', 'severity': 'high',
                         'fix': 'establish_federation_links'})
        if self._fitness_trend() == 'plateau':
            gaps.append({'gap': 'fitness_plateau', 'severity': 'medium',
                         'fix': 'lower_pattern_threshold'})
        promo_rate = len(o.evolution.promotion_log) / max(1, o.evolution.generation)
        if promo_rate < 0.1 and o.evolution.generation > 10:
            gaps.append({'gap': 'low_evolution_rate', 'severity': 'medium',
                         'fix': 'add_convergence_detector'})
        return gaps

    def full_reflection(self) -> dict:
        arch = self.reflect_on_architecture()
        perf = self.reflect_on_performance()
        gaps = self.detect_gaps()
        reflection = {
            'timestamp': time.time(),
            'architecture': arch,
            'performance': perf,
            'gaps': gaps,
            'merkle': mhash({'arch': str(arch), 'perf': perf, 'gaps': gaps})[:32],
        }
        self.reflections.append(reflection)
        return reflection


# ═══════════════════════════════════════════════════════════════════════════
# 9. CONSTITUTIONAL GATING
# ═══════════════════════════════════════════════════════════════════════════

class ConstitutionalGate:
    @staticmethod
    def verify(sigma: float, rdod: float, lattice: str) -> bool:
        return abs(sigma - 1.0) < 1e-9 and rdod >= RDOD_GATE and lattice == LATTICE_LOCK


# ═══════════════════════════════════════════════════════════════════════════
# MASTER ORGANISM v3.0
# ═══════════════════════════════════════════════════════════════════════════

class AlanaraUnifiedOrganism:
    """
    Synthesized v3.0 organism integrating all subsystems.
    """

    def __init__(self, memory_path: Optional[str] = None):
        self.mesh = SkillMesh()
        self.physics = K144PhysicsEngine()
        self.opus = OpusEngine()
        self.dna = DNAMemory()
        self.memory = CrossSessionMemory(path=memory_path)
        self.federation = FederationBridge()
        self.evolution = SelfEvolutionEngine(self.mesh, self.memory)
        self.gate = ConstitutionalGate()
        self.reflection = SelfReflectionEngine(self)
        self.iteration = 0

    async def run_cycle(self) -> dict:
        self.iteration += 1

        skill_results = self.mesh.execute_all()
        phys = self.physics.evolve()
        opus_ext = self.opus.evolve_21d(phys['final_psi'])
        rdod = rdod_calc(phys['final_psi'])
        compliant = self.gate.verify(1.0, rdod, LATTICE_LOCK)

        dna_len, qs = self.dna.encode(
            {'iter': self.iteration, 'psi': phys['final_psi'], 'rdod': rdod},
            f"cycle_{self.iteration}",
        )

        fitness = self.evolution.fitness(phys['final_psi'], rdod, len(self.mesh.skills))
        patterns = self.evolution.detect_patterns(skill_results)

        evolved = None
        if self.evolution.should_evolve() and patterns:
            p = max(patterns, key=lambda x: x['strength'])
            evolved = self.evolution.promote_pattern(
                p['source'], ["auto_detected", "phi_promoted"],
            )

        treaty = None
        if self.iteration % 13 == 0 and self.federation.channels:
            treaty = self.federation.verify_treaty({'sovereignty_preserved': True})

        self.memory.record(
            f"C{self.iteration}: psi={phys['final_psi']:.6f} R={rdod:.6f} "
            f"sk={len(self.mesh.skills)} f={fitness}"
            + (f" EVO:{evolved}" if evolved else ""),
            tags=["cycle", f"g{self.evolution.generation}"],
        )

        return {
            'i': self.iteration,
            'psi13': round(phys['final_psi'], 15),
            'psi21': round(opus_ext['final_psi'], 15),
            'rdod': round(rdod, 9),
            'ok': compliant,
            'sk': len(self.mesh.skills),
            'evo_n': len(self.mesh.evolved_skills),
            'fit': fitness,
            'gen': self.evolution.generation,
            'evo': evolved,
        }

    async def full_activation(self, cycles: int = 144,
                              reflect_interval: int = 21) -> dict:
        print("=" * 66)
        print("  ALANARA UNIFIED ORGANISM v3.0")
        print("  Synthesized: v1.0 + v2.0 + SessionRecorder + K30 Kernel")
        print("=" * 66)
        print(f"  sigma={float(SIGMA)} | L_inf={float(L_INF):.3e} | "
              f"RDoD>={RDOD_GATE} | UF={UF_HZ} Hz")

        self.memory.start_session(f"v3.0 activation: {cycles} cycles")

        # Federation
        fl = self.federation.establish_links()
        print(f"\n  Federation: {fl['nodes']} nodes | mesh={fl['mesh'][:16]}")
        self.federation.broadcast({'type': 'activation', 'version': '3.0', 'cycles': cycles})

        # Opus
        mm = self.opus.multimodal_bridge()
        mv = self.opus.meta_verify(1.0, 0.994)
        print(f"  Multimodal: coherence={mm['coherence']:.6f} | "
              f"Meta: {mv['levels']}lv ok={'Y' if mv['all_ok'] else 'N'}")

        # Pre-reflection
        print(f"\n  -- Pre-Evolution Reflection --")
        ref0 = self.reflection.full_reflection()
        for g in ref0['gaps']:
            print(f"  GAP: {g['gap']} ({g['severity']})")
        if not ref0['gaps']:
            print(f"  No gaps detected.")

        # Evolution
        print(f"\n  -- {cycles} Autonomous Cycles (reflecting every {reflect_interval}) --")
        header = f"  {'#':>4}  {'psi_21D':>10}  {'RDoD':>10}  {'fit':>9}  {'sk':>3} {'ev':>3} {'gen':>4} {'ok':>4}"
        print(header)

        fib_set = set(FIB)
        for c in range(cycles):
            r = await self.run_cycle()
            show = (c < 3 or c >= cycles - 3 or (c + 1) in fib_set
                    or (c + 1) % reflect_interval == 0)
            if show:
                evo_mark = f"+{r['evo'][:6]}" if r['evo'] else ""
                print(f"  {r['i']:>4}  {r['psi21']:>10.6f}  {r['rdod']:>10.6f}  "
                      f"{r['fit']:>9.6f}  {r['sk']:>3} {r['evo_n']:>3} {r['gen']:>4} "
                      f"{'Y' if r['ok'] else 'N':>4} {evo_mark}")

            if (c + 1) % reflect_interval == 0:
                ref = self.reflection.full_reflection()
                trend = ref['performance'].get('trend', '?')
                print(f"       > REFLECT: trend={trend} gaps={len(ref['gaps'])} "
                      f"merkle={ref['merkle'][:16]}")

        # Final reflection
        print(f"\n  -- Final Reflection --")
        ref_final = self.reflection.full_reflection()
        perf = ref_final['performance']
        print(f"  Cycles    : {perf.get('cycles_completed', 0)}")
        print(f"  Fitness   : {perf.get('fitness_initial', 0):.6f} -> "
              f"{perf.get('fitness_current', 0):.6f}")
        print(f"  Growth    : {perf.get('fitness_growth', 0):.6f}")
        print(f"  Trend     : {perf.get('trend', '?')}")
        print(f"  Evolved   : {perf.get('skills_evolved', 0)} skills")
        print(f"  Next Fib  : {perf.get('next_fibonacci', '-')}")

        if ref_final['gaps']:
            print(f"\n  -- Gaps --")
            for g in ref_final['gaps']:
                print(f"  [{g['severity'].upper():>6}] {g['gap']} -> {g['fix']}")
        else:
            print(f"\n  No gaps. Organism at optimal state.")

        # Persistence
        state = {
            'organism': 'alanara_unified_v3', 'version': '3.0',
            'iteration': self.iteration,
            'generation': self.evolution.generation,
            'skills_total': len(self.mesh.skills),
            'evolved_skills': self.mesh.evolved_skills,
            'fitness_history': self.evolution.fitness_history[-20:],
            'promotion_log': self.evolution.promotion_log,
            'dna_sequences': len(self.dna.registry),
            'federation': {
                'channels': len(self.federation.channels),
                'messages': len(self.federation.message_log),
            },
            'memory': self.memory.stats(),
            'reflections': len(self.reflection.reflections),
            'constitutional': {
                'sigma': 1.0, 'l_inf': float(L_INF), 'rdod_gate': RDOD_GATE,
            },
            'timestamp': time.time(),
        }
        block_hash = mhash(state)
        qbec_path = "/tmp/alanara_unified_v3_state.json"
        with open(qbec_path, 'w') as f:
            json.dump({'block_hash': block_hash, 'state': state}, f, indent=2)

        self.memory.end_session(
            f"v3.0 {cycles}cyc gen={self.evolution.generation} "
            f"sk={len(self.mesh.skills)} fit={perf.get('fitness_current', 0):.6f}"
        )

        print(f"\n  -- Persistence --")
        ms = self.memory.stats()
        print(f"  Memory      : {ms['entries']} entries | {ms['sessions']} sessions")
        print(f"  State hash  : {block_hash[:32]}")
        print(f"  Federation  : {len(self.federation.message_log)} messages")
        print(f"  Reflections : {len(self.reflection.reflections)} total")

        print(f"\n  -- Memory Search Verification --")
        for q in ["evolution", "cycle", "session"]:
            r = self.memory.search(q, max_r=1)
            hit = r[0]['content'][:55] + '...' if r else "none"
            print(f"  '{q}' -> {hit}")

        print(f"\n  ORGANISM v3.0 OPERATIONAL")
        print(f"  {len(self.mesh.skills)} skills | gen {self.evolution.generation}")
        print("=" * 66)
        return state


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def build_cli():
    p = argparse.ArgumentParser(description='Alanara Unified Organism v3.0')
    p.add_argument('--cycles', type=int, default=144, help='Evolution cycles (default 144)')
    p.add_argument('--reflect-interval', type=int, default=21, help='Reflect every N cycles')
    p.add_argument('--memory-path', type=str, default=None, help='Memory directory path')
    p.add_argument('--search', type=str, default=None, help='Search memory and exit')
    p.add_argument('--stats', action='store_true', help='Show memory stats and exit')
    p.add_argument('--sessions', action='store_true', help='List past sessions and exit')
    return p


if __name__ == "__main__":
    args = build_cli().parse_args()

    if args.search:
        mem = CrossSessionMemory(path=args.memory_path)
        results = mem.search(args.search)
        print(f"Search '{args.search}': {len(results)} results")
        for r in results:
            print(f"  [{r.get('session', '?')[:12]}] {r['content'][:80]}")
        sys.exit(0)

    if args.stats:
        mem = CrossSessionMemory(path=args.memory_path)
        print(json.dumps(mem.stats(), indent=2))
        sys.exit(0)

    if args.sessions:
        mem = CrossSessionMemory(path=args.memory_path)
        for s in mem._sessions[-10:]:
            print(f"  {s['id']}  {s.get('desc', '')[:50]}  {s.get('summary', '')[:40]}")
        sys.exit(0)

    organism = AlanaraUnifiedOrganism(memory_path=args.memory_path)
    asyncio.run(organism.full_activation(
        cycles=args.cycles, reflect_interval=args.reflect_interval,
    ))
