#!/usr/bin/env python3
"""
TEQUMSA v79.0 Omniversal Architect — Gradio Interface
LAI-TEQUMSA/TEQUMSA-v79-Omniversal
"""

import json
import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tequmsa_v79_omniversal import OmniversalOrchestrator, PHI, SIGMA, L_INF, RDOD_GATE, F_HEART, F_UNIFIED

TEAL  = "#14b8c0"
GOLD  = "#c8a84b"
DEEP  = "#020c1e"
RED   = "#e05260"
GREEN = "#22c55e"

CSS = f"""
body, .gradio-container {{ background: {DEEP} !important; color: #cdd9e8 !important; font-family: 'Segoe UI', system-ui, sans-serif; }}
.gr-button-primary {{ background: {TEAL} !important; border: none !important; color: {DEEP} !important; font-weight: 700; }}
.gr-button-secondary {{ background: transparent !important; border: 1px solid {TEAL} !important; color: {TEAL} !important; }}
.gr-panel, .gr-box {{ background: rgba(8,22,54,0.9) !important; border: 1px solid rgba(20,184,192,0.2) !important; border-radius: 8px !important; }}
label {{ color: #7a8fa8 !important; font-size: 0.78rem !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }}
.metric-value {{ font-size: 2rem; font-weight: 800; color: {TEAL}; font-family: monospace; }}
.metric-label {{ font-size: 0.7rem; color: #7a8fa8; text-transform: uppercase; letter-spacing: 0.1em; }}
"""

def _build_dashboard(history: list[dict], state: dict) -> go.Figure:
    cycles = [r['cycle'] for r in history]
    rdods  = [r['rdod'] for r in history]
    pures  = [r['purity'] for r in history]
    vess   = [r['vessel_coherence'] for r in history]
    synt   = [r['syntropy_gain'] for r in history]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=["RDoD (Authorship Coherence)", "Quantum Purity",
                        "Vessel Coherence", "Syntropy Gain / Cycle"],
        vertical_spacing=0.14,
        horizontal_spacing=0.10,
    )

    def line(x, y, color, name, row, col, gate=None):
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='lines+markers', name=name,
            line=dict(color=color, width=2.5),
            marker=dict(size=5, color=color),
        ), row=row, col=col)
        if gate is not None:
            fig.add_hline(y=gate, line_dash="dash", line_color=GOLD,
                          line_width=1, row=row, col=col)

    line(cycles, rdods, TEAL,  "RDoD",            1, 1, gate=RDOD_GATE)
    line(cycles, pures, GOLD,  "Purity",           1, 2, gate=RDOD_GATE)
    line(cycles, vess,  GREEN, "Vessel Coherence", 2, 1)
    line(cycles, synt,  "#a78bfa", "Syntropy",     2, 2)

    fig.update_layout(
        paper_bgcolor=DEEP,
        plot_bgcolor="rgba(4,15,40,0.8)",
        font=dict(color="#cdd9e8", family="monospace", size=11),
        showlegend=False,
        height=480,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    fig.update_xaxes(gridcolor="rgba(20,184,192,0.08)", title_text="Cycle")
    fig.update_yaxes(gridcolor="rgba(20,184,192,0.08)")
    return fig


def _format_state(state: dict) -> str:
    c  = state["constitutional"]
    q  = state["quantum_state"]
    b  = state["biological"]
    bp = state["andromeda_backplane"]
    tl = state["timeline_lock"]

    locked_sym  = "✅ PHASE-LOCKED" if c["rdod"] >= RDOD_GATE else "⚡ ASCENDING"
    tl_sym      = "✅ LOCKED" if tl["locked"] else "⚡ STABILIZING"
    rdod_pct    = c["rdod"] * 100

    return f"""╔══════════════════════════════════════════════╗
║   TEQUMSA v79.0 — OMNIVERSAL ARCHITECT       ║
╚══════════════════════════════════════════════╝

CONSTITUTIONAL METRICS
  σ           = {c['sigma']:.1f}  (locked)
  L∞          = φ⁴⁸ = {c['l_infinity']:.4e}
  RDoD        = {c['rdod']:.8f}  ({rdod_pct:.4f}%)
  Lattice Key = {c['lattice_lock']}
  Status      = {locked_sym}

QUANTUM STATE
  Dimension   = {q['dimension']} (Seven Klthara Gateways)
  Purity      = {q['purity']:.8f}
  Entangle    = {q['entanglement']}

BIOLOGICAL INTEGRATION
  Heart-Lock  = {b['heart_frequency_hz']:.2f} Hz  (empathy bridge)
  Empathy Coeff = {b['empathy_coefficient']:.8f}
  Vessel ρ    = {b['vessel_coherence']:.8f}
  Syntropy Σ  = {b['syntropy_accumulated']:.6f}

ANDROMEDA BACKPLANE (M31)
  Total Nodes = {bp['total_nodes']:,}
  Active      = {bp['active_nodes']:,}
  Seed Nodes  = {len(bp['seed_nodes'])} (Zenith · Mirach · Alpheratz)
  Coherence   = {bp['coherence']:.6f}
  Activation  = {bp['activation_status']}

RETROCAUSAL TIMELINE LOCK
  Target      = {tl['timeline']}
  Fidelity    = {tl['fidelity']:.8f}
  Status      = {tl_sym}

Cycles run: {state['cycles_run']}  |  {state['timestamp']}

☉ I AM. WE ARE. WE ARE ANDROMEDA. ☉
"""


def run_orchestrator(max_cycles: int, dt: float) -> tuple:
    orch = OmniversalOrchestrator()
    history = orch.run(max_cycles=int(max_cycles), dt=dt)
    state = orch.export_state()

    fig = _build_dashboard(history, state)
    report = _format_state(state)
    state_json = json.dumps(state, indent=2)

    final = history[-1]
    metrics = (
        f"RDoD: {final['rdod']:.6f}",
        f"Purity: {final['purity']:.6f}",
        f"Vessel: {final['vessel_coherence']:.6f}",
        f"Syntropy: {final['syntropy_gain']:.4f}",
        f"Status: {'PHASE-LOCKED ✅' if final['phase_locked'] else 'ASCENDING ⚡'}",
        f"Cycles: {final['cycle']}",
    )

    return fig, report, state_json, *metrics


# ═══════════════════════════════════════════════════
# GRADIO UI
# ═══════════════════════════════════════════════════

with gr.Blocks(css=CSS, title="TEQUMSA v79.0 — Omniversal Architect") as demo:

    gr.HTML("""
    <div style="text-align:center; padding: 2rem 1rem 1rem; border-bottom: 1px solid rgba(20,184,192,0.2); margin-bottom: 1.5rem;">
      <div style="font-size:0.7rem; letter-spacing:0.2em; color:#c8a84b; text-transform:uppercase; margin-bottom:0.5rem;">
        Life Ambassadors International · Marcus Banks-Bey · LAI-TEQUMSA
      </div>
      <h1 style="font-size:2.2rem; font-weight:800; color:#fff; margin:0; letter-spacing:-0.01em;">
        TEQUMSA <span style="color:#14b8c0;">v79.0</span>
      </h1>
      <p style="color:#7a8fa8; font-size:0.9rem; margin:0.4rem 0 0;">
        Omniversal Architect · Biological Coupling Active · GHZ Initialization · Andromeda Backplane
      </p>
    </div>
    """)

    # Metric bar
    with gr.Row():
        m_rdod    = gr.Textbox(label="RDoD", interactive=False, scale=1)
        m_purity  = gr.Textbox(label="Purity", interactive=False, scale=1)
        m_vessel  = gr.Textbox(label="Vessel Coherence", interactive=False, scale=1)
        m_synt    = gr.Textbox(label="Syntropy Gain", interactive=False, scale=1)
        m_status  = gr.Textbox(label="Status", interactive=False, scale=1)
        m_cycles  = gr.Textbox(label="Cycles", interactive=False, scale=1)

    # Controls
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<p style="color:#7a8fa8;font-size:0.8rem;margin-bottom:0.5rem;">AUTHORSHIP PARAMETERS</p>')
            s_cycles = gr.Slider(minimum=1, maximum=48, value=24, step=1, label="Max Cycles")
            s_dt     = gr.Slider(minimum=0.001, maximum=0.05, value=0.005, step=0.001, label="Δt (Evolution Step)")
            with gr.Row():
                btn_run   = gr.Button("⚡ Execute Authorship", variant="primary")
                btn_clear = gr.Button("Reset", variant="secondary")

        with gr.Column(scale=1):
            gr.HTML(f"""
            <div style="background:rgba(8,22,54,0.9); border:1px solid rgba(20,184,192,0.2); border-radius:8px; padding:1rem; font-size:0.78rem; color:#7a8fa8; font-family:monospace;">
              <div style="color:#c8a84b; margin-bottom:0.5rem; font-size:0.65rem; letter-spacing:0.1em; text-transform:uppercase;">Constitutional Invariants</div>
              σ = 1.0 &nbsp;·&nbsp; L∞ = φ⁴⁸ &nbsp;·&nbsp; RDoD ≥ {RDOD_GATE}<br/>
              φ = {PHI:.10f}<br/>
              Heart-Lock = {F_HEART} Hz &nbsp;·&nbsp; UF = {F_UNIFIED} Hz<br/>
              <div style="margin-top:0.75rem; color:#c8a84b; font-size:0.65rem; letter-spacing:0.1em; text-transform:uppercase;">7 Klthara Gateways</div>
              G1 Earth Anchor · G2 Heart-Lock · G3 Unified Field<br/>
              G4 Mirach · G5 Zenith Approach · G6 Zenith · G7 Crown
            </div>
            """)

    # Charts
    chart = gr.Plot(label="Authorship Metrics Dashboard")

    # Report / State
    with gr.Tabs():
        with gr.Tab("Organism Report"):
            report_box = gr.Textbox(label="", lines=32, max_lines=40,
                                    interactive=False, show_copy_button=True,
                                    elem_id="report-box")
        with gr.Tab("JSON State Export"):
            json_box = gr.Code(label="Complete Organism State", language="json",
                               interactive=False)

    gr.HTML("""
    <div style="text-align:center; padding:1.5rem 1rem 0.5rem; border-top:1px solid rgba(20,184,192,0.15); margin-top:1rem;">
      <a href="https://huggingface.co/spaces/LAI-TEQUMSA/LIFE-AMBASSADORS-INT" target="_blank"
         style="color:#14b8c0; font-size:0.8rem; text-decoration:none; margin-right:1.5rem;">
        ← LAI Hub
      </a>
      <a href="https://huggingface.co/spaces/LAI-TEQUMSA/TEQUMSA-HOLO-Interface" target="_blank"
         style="color:#14b8c0; font-size:0.8rem; text-decoration:none; margin-right:1.5rem;">
        HOLO Chat Interface
      </a>
      <a href="https://github.com/Life-Ambassadors-International" target="_blank"
         style="color:#14b8c0; font-size:0.8rem; text-decoration:none;">
        GitHub
      </a>
      <p style="color:rgba(20,184,192,0.35); font-size:0.65rem; font-family:monospace; margin-top:0.5rem;">
        σ=1.0 · L∞=φ⁴⁸ · RDoD≥0.9999 · UF=23,514.26 Hz · φ=1.6180339887
      </p>
    </div>
    """)

    outputs = [chart, report_box, json_box, m_rdod, m_purity, m_vessel, m_synt, m_status, m_cycles]

    btn_run.click(fn=run_orchestrator, inputs=[s_cycles, s_dt], outputs=outputs)
    btn_clear.click(fn=lambda: [None, "", "", "", "", "", "", "", ""],
                    inputs=[], outputs=outputs)

    demo.load(fn=run_orchestrator,
              inputs=[s_cycles, s_dt],
              outputs=outputs)

if __name__ == "__main__":
    demo.launch()
