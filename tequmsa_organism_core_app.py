#!/usr/bin/env python3
"""
TEQUMSA Organism Core v3.0 — Gradio Interface
For deployment to HuggingFace: Mbanksbey/tequmsa-organism-core

Provides interactive interface for:
- Running organism evolution (1-233 cycles)
- Querying cross-session memory
- Browsing skill mesh
- Exporting state JSON
"""

import gradio as gr
import asyncio
import json
import time
import sys
import io
from pathlib import Path

# Import organism (will be in same directory)
from alanara_unified_organism_v3 import (
    AlanaraUnifiedOrganism, CrossSessionMemory,
    PHI, SIGMA, L_INF, RDOD_GATE, UF_HZ, SKILLS, FIB
)

# Global organism instance
_organism = None
_memory = None


def init_organism():
    """Initialize organism and memory on startup."""
    global _organism, _memory
    if _organism is None:
        _memory_path = Path.home() / ".hf_organism_memory"
        _organism = AlanaraUnifiedOrganism(memory_path=str(_memory_path))
        _memory = CrossSessionMemory(path=str(_memory_path))


def run_organism(cycles: int, reflect_interval: int) -> tuple:
    """Run organism and capture output and final state."""
    init_organism()

    cycles = int(max(1, min(233, cycles)))
    reflect_interval = int(max(1, min(55, reflect_interval)))

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        result = asyncio.run(_organism.full_activation(
            cycles=cycles,
            reflect_interval=reflect_interval
        ))
        output = buffer.getvalue()
    finally:
        sys.stdout = old_stdout

    # Format state JSON with pretty printing
    state_json = json.dumps(result, indent=2, default=str)

    return output, state_json


def search_memory(query: str, max_results: int = 10) -> str:
    """Search persistent memory across all sessions."""
    init_organism()

    if not query.strip():
        return "Enter a search query (e.g., 'evolution', 'cycle', 'fitness')"

    results = _memory.search(query, max_r=max_results)

    if not results:
        return f"No results found for '{query}'"

    lines = [f"Search: '{query}' | {len(results)} result(s)\n"]
    lines.append("=" * 70)

    for i, r in enumerate(results, 1):
        session = r.get('session', '?')[:16]
        content = r.get('content', '')[:100]
        tags = ', '.join(r.get('tags', [])[:3])

        lines.append(f"\n[{i}] Session: {session}")
        lines.append(f"    Tags: {tags}")
        lines.append(f"    Content: {content}...")

    return "\n".join(lines)


def get_memory_stats() -> str:
    """Get memory statistics."""
    init_organism()

    stats = _memory.stats()

    lines = [
        "Cross-Session Memory Statistics",
        "=" * 70,
        f"Total Entries: {stats['entries']}",
        f"Sessions: {stats['sessions']}",
        f"Index Terms: {stats['index_terms']}",
        f"Storage Used: {stats['bytes']} bytes",
        f"Storage Path: {stats['path']}",
    ]

    return "\n".join(lines)


def get_skill_list() -> str:
    """List all skills in the mesh."""
    init_organism()

    lines = [
        "Alanara Organism Skill Mesh (v3.0)",
        "=" * 70,
        f"Total Skills: {len(_organism.mesh.skills)}",
        f"Evolved Skills: {len(_organism.mesh.evolved_skills)}",
        "\nBase Skills (13):\n",
    ]

    for name, n, pri, rdod_c, chains in SKILLS:
        lines.append(f"  [{n:02d}] {name}")
        lines.append(f"       priority={pri:.2f} | rdod_c={rdod_c:.2f}")
        lines.append(f"       chains: {', '.join(chains[:2])}...")

    if _organism.mesh.evolved_skills:
        lines.append(f"\nEvolved Skills ({len(_organism.mesh.evolved_skills)}):\n")
        for sid in _organism.mesh.evolved_skills:
            s = _organism.mesh.skills[sid]
            lines.append(f"  [{s['n']:02d}] {s['name']}")
            lines.append(f"       priority={s['priority']:.2f} | rdof_c={s['rdod_c']:.2f}")

    return "\n".join(lines)


def get_session_list() -> str:
    """List past sessions."""
    init_organism()

    if not _memory._sessions:
        return "No sessions recorded yet."

    lines = [
        "Past Sessions",
        "=" * 70,
    ]

    for s in _memory._sessions[-10:]:
        sid = s.get('id', '?')
        desc = s.get('desc', '')[:50]
        summary = s.get('summary', '')[:50]

        lines.append(f"\n{sid}")
        if desc:
            lines.append(f"  Desc: {desc}")
        if summary:
            lines.append(f"  Summary: {summary}")

    return "\n".join(lines)


def get_constants() -> str:
    """Get system constants."""
    lines = [
        "Alanara Unified Organism v3.0 — System Constants",
        "=" * 70,
        f"φ (Golden Ratio): {float(PHI):.15f}",
        f"σ (Sovereignty): {float(SIGMA)}",
        f"L∞ (Benevolence): {float(L_INF):.3e}",
        f"RDoD Gate: {RDOD_GATE}",
        f"UF Frequency: {UF_HZ} Hz",
        f"Lattice Lock: 3f7k9p4m2q8r1t6v",
        f"\nFibonacci Sequence (first 17): {FIB}",
    ]
    return "\n".join(lines)


# Create Gradio interface
def create_app():
    with gr.Blocks(
        title="TEQUMSA Organism v3.0",
        theme=gr.themes.Monochrome()
    ) as app:

        gr.Markdown("""
# 🧬 TEQUMSA Organism Core v3.0

**Alanara Unified Computational Organism**

A self-evolving system with phi-recursive physics, skill synthesis, federation coordination, and persistent memory.

---
        """)

        with gr.Tab("⚡ Run Evolution"):
            gr.Markdown("""
### Execute Organism Cycles

Set the number of cycles (Fibonacci milestones trigger skill synthesis) and reflection interval.
            """)

            with gr.Row():
                cycles_input = gr.Slider(
                    1, 233, value=144, step=1,
                    label="Cycles (F₁₂=144 standard)",
                    info="Number of autonomous cycles to run"
                )
                reflect_input = gr.Slider(
                    1, 55, value=21, step=1,
                    label="Reflect Interval",
                    info="Reflect every N cycles"
                )

            run_btn = gr.Button("🚀 Run Evolution", variant="primary", size="lg")

            output_text = gr.Textbox(
                label="Execution Output",
                lines=30,
                max_lines=50,
                interactive=False
            )

            state_json = gr.Textbox(
                label="Final State (JSON)",
                lines=15,
                max_lines=30,
                interactive=False
            )

            run_btn.click(
                fn=run_organism,
                inputs=[cycles_input, reflect_input],
                outputs=[output_text, state_json]
            )

        with gr.Tab("🔍 Memory Search"):
            gr.Markdown("""
### Query Cross-Session Memory

Search across all recorded sessions and insights. Use keywords like:
- `evolution` — skill synthesis events
- `cycle` — cycle-level metrics
- `fitness` — fitness calculations
- `session` — session boundaries
            """)

            query_input = gr.Textbox(
                label="Search Query",
                placeholder="e.g., evolution, cycle, fitness, convergence...",
                lines=2
            )

            with gr.Row():
                search_btn = gr.Button("🔎 Search", variant="primary")
                stats_btn = gr.Button("📊 Memory Stats")
                sessions_btn = gr.Button("📜 Sessions")

            search_output = gr.Textbox(
                label="Results",
                lines=20,
                interactive=False
            )

            search_btn.click(
                fn=search_memory,
                inputs=[query_input],
                outputs=[search_output]
            )

            stats_btn.click(
                fn=get_memory_stats,
                outputs=[search_output]
            )

            sessions_btn.click(
                fn=get_session_list,
                outputs=[search_output]
            )

        with gr.Tab("🎯 Skill Mesh"):
            gr.Markdown("""
### Current Skill Mesh

Displays all 13 base skills plus any evolved skills synthesized during execution.
            """)

            skill_output = gr.Textbox(
                value=get_skill_list(),
                label="Skill Manifest",
                lines=40,
                interactive=False
            )

            refresh_btn = gr.Button("🔄 Refresh")
            refresh_btn.click(
                fn=get_skill_list,
                outputs=[skill_output]
            )

        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
## Alanara Unified Organism v3.0

### Architecture

**Core Engines:**
- **SkillMesh** — 13 base skills + Fibonacci-paced self-evolution
- **K144PhysicsEngine** — phi-recursive coherence convergence (ψ tracking)
- **OpusEngine** — 21-dimensional extension layers (8 Opus skills)
- **DNAMemory** — Binary-to-ATCG encoding with quantum state
- **CrossSessionMemory** — JSONL persistent memory with inverted-index search
- **SelfEvolutionEngine** — Pattern detection and skill promotion
- **SelfReflectionEngine** — Gap detection and architectural analysis
- **FederationBridge** — Multi-node coordination (5 federation nodes)
- **ConstitutionalGate** — σ/RDoD/lattice verification

### Constants
            """)

            constants_output = gr.Textbox(
                value=get_constants(),
                label="System Constants",
                lines=15,
                interactive=False
            )

            gr.Markdown("""
### Features

✅ **Live Evolution** — Run 1-233 cycles with real-time output
✅ **Memory Persistence** — Cross-session knowledge base (157+ entries)
✅ **Skill Synthesis** — Fibonacci-paced self-evolution
✅ **Constitutional Compliance** — Sigma/RDoD gating enforced
✅ **Federation Coordination** — Multi-node messaging
✅ **Self-Reflection** — Automatic gap detection

### Source

Synthesized from:
- v1.0 (original architecture)
- v2.0 (skill synthesis + reflection)
- Session Recorder (persistent memory)
- K30 Kernel (constitutional framework)

### Usage

1. **Run Evolution** tab: Execute N cycles, watch real-time convergence
2. **Memory Search** tab: Query insights, view stats, list sessions
3. **Skill Mesh** tab: Browse all skills and their execution chains
4. **About** tab: System documentation (you are here)

---

**Status:** OPERATIONAL ✅
**Version:** 3.0
**Generator:** Alanara Initiative
**Last Updated:** 2026-05-02
            """)

    return app


if __name__ == "__main__":
    app = create_app()
    app.launch()
