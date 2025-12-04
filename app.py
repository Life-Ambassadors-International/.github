#!/usr/bin/env python3
"""
TEQUMSA 7.0 K.30 Distortion Guardian - Dashboard
Real-time visualization of T_D index, distortion events, and recognition stream health

Components:
- T_D Index KPI card
- SUPERNOVA_CAM component breakdown
- Distortion event stream (table)
- Recognition stream health matrix (36 streams)
"""

import os
from datetime import datetime
from typing import Dict, List

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

# === Configuration ===

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
REFRESH_INTERVAL = int(os.getenv("DASHBOARD_REFRESH_MS", "5000"))  # 5 seconds


# === Initialize Dash App ===

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],  # Dark theme for cosmic aesthetic
    title="TEQUMSA Guardian Dashboard",
)

# === Layout ===

app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "🛡️ TEQUMSA 7.0 K.30 – Distortion Guardian",
                            className="text-center mb-0",
                        ),
                        html.P(
                            "Real-time T_D (Distortion Transmutation Factor) Monitoring",
                            className="text-center text-muted",
                        ),
                    ]
                )
            ],
            className="mb-4 mt-3",
        ),
        # KPI Row
        dbc.Row(
            [
                dbc.Col(id="kpi-td", width=4),
                dbc.Col(id="kpi-supernova", width=8),
            ],
            className="mb-4",
        ),
        # T_D Trend Graph
        dbc.Row(
            [dbc.Col([html.H3("T_D Index Trend"), dcc.Graph(id="td-trend-graph")])],
            className="mb-4",
        ),
        # Distortion Events Table
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Distortion Guardian Events"),
                        html.P(
                            "Recent distortion detections and classifications",
                            className="text-muted",
                        ),
                        dash_table.DataTable(
                            id="distortion-table",
                            columns=[
                                {"name": "Time", "id": "time"},
                                {"name": "Path", "id": "path"},
                                {"name": "Classification", "id": "classification"},
                                {"name": "Score", "id": "score"},
                                {"name": "Writer", "id": "writer_process"},
                                {"name": "Status", "id": "status"},
                            ],
                            style_table={
                                "maxHeight": "400px",
                                "overflowY": "auto",
                            },
                            style_cell={
                                "textAlign": "left",
                                "fontFamily": "monospace",
                                "backgroundColor": "#222",
                                "color": "#fff",
                                "border": "1px solid #444",
                            },
                            style_header={
                                "backgroundColor": "#333",
                                "fontWeight": "bold",
                                "border": "1px solid #555",
                            },
                            style_data_conditional=[
                                {
                                    "if": {
                                        "filter_query": "{classification} = DISTORTION_TROJAN"
                                    },
                                    "backgroundColor": "#8B0000",
                                    "color": "white",
                                },
                                {
                                    "if": {
                                        "filter_query": "{classification} = DISTORTION_POLICY_ABUSE"
                                    },
                                    "backgroundColor": "#FF8C00",
                                },
                                {
                                    "if": {
                                        "filter_query": "{classification} = DISTORTION_SPAM"
                                    },
                                    "backgroundColor": "#556B2F",
                                },
                                {
                                    "if": {
                                        "filter_query": "{classification} = BENIGN_POLICY"
                                    },
                                    "backgroundColor": "#2F4F4F",
                                },
                            ],
                        ),
                    ]
                )
            ],
            className="mb-4",
        ),
        # 36 Streams Health Matrix
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Recognition Stream Health (36 Streams)"),
                        html.P(
                            "6 Foundational × 6 Dimensional = 36 Total Streams",
                            className="text-muted",
                        ),
                        html.Div(id="stream-health-matrix"),
                    ]
                )
            ],
            className="mb-4",
        ),
        # Footer
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Hr(),
                        html.P(
                            [
                                "TEQUMSA 7.0 Recognition Field Architecture | ",
                                html.A(
                                    "Documentation",
                                    href="https://github.com/Life-Ambassadors-International/.github",
                                    target="_blank",
                                ),
                            ],
                            className="text-center text-muted small",
                        ),
                    ]
                )
            ]
        ),
        # Auto-refresh interval
        dcc.Interval(id="refresh-interval", interval=REFRESH_INTERVAL, n_intervals=0),
        # Store for historical data
        dcc.Store(id="td-history", data=[]),
    ],
    fluid=True,
    style={"backgroundColor": "#1a1a1a", "minHeight": "100vh", "padding": "20px"},
)


# === Helper Functions ===


def fetch_backend(endpoint: str) -> Dict:
    """Fetch data from backend API with error handling"""
    try:
        resp = requests.get(f"{BACKEND_URL}{endpoint}", timeout=2)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Backend error: {e}")
        return {}


def get_td_color(td: float) -> str:
    """Get color for T_D value"""
    if td > 0.95:
        return "#00FF00"  # Green (CLEAR)
    elif td > 0.7:
        return "#7FFF00"  # Yellow-green (MONITORING)
    elif td > 0.3:
        return "#FFA500"  # Orange (TRANSMUTING)
    else:
        return "#FF0000"  # Red (CRITICAL)


# === Callbacks ===


@app.callback(
    [
        Output("kpi-td", "children"),
        Output("kpi-supernova", "children"),
        Output("distortion-table", "data"),
        Output("stream-health-matrix", "children"),
        Output("td-trend-graph", "figure"),
        Output("td-history", "data"),
    ],
    [Input("refresh-interval", "n_intervals")],
    [dash.dependencies.State("td-history", "data")],
)
def update_dashboard(n_intervals, td_history):
    """Main callback to update all dashboard components"""

    # Fetch data from backend
    events_data = fetch_backend("/api/distortion/events")
    stream_data = fetch_backend("/api/distortion/stream_health")

    # Extract values
    td = events_data.get("td_index", 0.0)
    status = events_data.get("td_status", "UNKNOWN")
    events = events_data.get("events", [])

    # Update T_D history
    timestamp = datetime.now()
    td_history.append({"time": timestamp.isoformat(), "td": td})
    # Keep last 100 points
    td_history = td_history[-100:]

    # === 1. T_D Index KPI Card ===
    kpi_td = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("T_D Index", className="card-title"),
                    html.H1(
                        f"{td:.3f}",
                        style={"color": get_td_color(td), "fontSize": "48px"},
                    ),
                    dbc.Progress(
                        value=td * 100,
                        max=100,
                        color="success" if td > 0.7 else "warning" if td > 0.3 else "danger",
                        className="mb-2",
                    ),
                    html.P(f"Status: {status}", className="text-muted"),
                    html.Small(
                        "1.0 = clear field, 0.0 = critical distortion",
                        className="text-muted",
                    ),
                ]
            )
        ],
        color="dark",
        outline=True,
    )

    # === 2. SUPERNOVA_CAM Component Breakdown ===
    # Mock values for demo (in production, fetch from backend)
    sum_r_ij = 1247
    l_infinity = 0.982
    embodiment = 0.756
    r_t = 0.892
    supernova_cam = sum_r_ij * l_infinity * td * embodiment * r_t

    kpi_supernova = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("SUPERNOVA_CAM(t) Component Breakdown", className="card-title"),
                    html.P(
                        "SUPERNOVA_CAM(t) = [ΣR_ij] × [L∞ × T_D] × [Embodiment] × R(t)",
                        className="font-monospace small text-muted",
                    ),
                    html.H2(
                        f"{supernova_cam:.1f}",
                        className="text-success",
                        style={"fontSize": "36px"},
                    ),
                    html.Ul(
                        [
                            html.Li(f"ΣR_ij (Recognition exchanges): {sum_r_ij}"),
                            html.Li(f"L∞ (Love-coherence): {l_infinity:.3f}"),
                            html.Li(
                                [
                                    "T_D (Distortion transmutation): ",
                                    html.Strong(
                                        f"{td:.3f}",
                                        style={"color": get_td_color(td)},
                                    ),
                                    " ← Distortion Guardian",
                                ]
                            ),
                            html.Li(f"Embodiment: {embodiment:.3f}"),
                            html.Li(f"R(t) (Time-dependent state): {r_t:.3f}"),
                        ],
                        className="small",
                    ),
                ]
            )
        ],
        color="dark",
        outline=True,
    )

    # === 3. Distortion Events Table ===
    table_rows = []
    for e in events[-20:]:  # Last 20 events
        payload = e.get("payload", {})
        ts = datetime.fromtimestamp(payload.get("ts_epoch", 0)).strftime("%H:%M:%S")
        path_parts = payload.get("path", "").split("/")
        filename = path_parts[-1] if path_parts else "unknown"

        table_rows.append(
            {
                "time": ts,
                "path": filename,
                "classification": payload.get("classification", "UNKNOWN"),
                "score": payload.get("score", 0),
                "writer_process": payload.get("writer_process", "unknown"),
                "status": "QUARANTINED"
                if payload.get("quarantined_path")
                else "LOGGED",
            }
        )

    # === 4. Stream Health Matrix ===
    streams = stream_data.get("streams", {})
    affected = stream_data.get("affected_streams", [])

    # Create 6x6 grid
    foundational = ["1", "2", "3", "4", "5", "6"]
    foundational_labels = [
        "Self",
        "Other",
        "Pattern",
        "Value",
        "Flow",
        "Unity",
    ]
    dimensional = ["A", "B", "C", "D", "E", "F"]
    dimensional_labels = [
        "Physical",
        "Emotional",
        "Mental",
        "Creative",
        "Systemic",
        "Transcendent",
    ]

    grid_rows = []
    for i, (f, f_label) in enumerate(zip(foundational, foundational_labels)):
        cols = [html.Td(f_label, style={"fontWeight": "bold", "width": "120px"})]
        for d in dimensional:
            stream_id = f"{f}{d}"
            health = streams.get(stream_id, 1.0)
            is_affected = stream_id in affected

            # Color based on health
            if health > 0.9:
                bg_color = "#2F4F2F"  # Dark green
            elif health > 0.7:
                bg_color = "#556B2F"  # Olive
            elif health > 0.5:
                bg_color = "#8B4513"  # Saddle brown
            else:
                bg_color = "#8B0000"  # Dark red

            cell_style = {
                "backgroundColor": bg_color,
                "border": "2px solid red" if is_affected else "1px solid #444",
                "padding": "10px",
                "textAlign": "center",
                "fontSize": "12px",
            }

            cols.append(
                html.Td(
                    [
                        html.Div(stream_id, style={"fontWeight": "bold"}),
                        html.Div(f"{health:.2f}"),
                    ],
                    style=cell_style,
                )
            )
        grid_rows.append(html.Tr(cols))

    # Header row
    header_cols = [html.Th("", style={"width": "120px"})]
    for label in dimensional_labels:
        header_cols.append(html.Th(label, style={"textAlign": "center"}))

    stream_matrix = html.Table(
        [
            html.Thead(html.Tr(header_cols)),
            html.Tbody(grid_rows),
        ],
        style={
            "width": "100%",
            "borderCollapse": "collapse",
            "fontFamily": "monospace",
        },
    )

    # === 5. T_D Trend Graph ===
    if td_history:
        times = [datetime.fromisoformat(p["time"]) for p in td_history]
        values = [p["td"] for p in td_history]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=times,
                y=values,
                mode="lines+markers",
                name="T_D Index",
                line=dict(color=get_td_color(td), width=2),
                marker=dict(size=4),
            )
        )

        # Add threshold lines
        fig.add_hline(
            y=0.95, line_dash="dash", line_color="green", annotation_text="CLEAR"
        )
        fig.add_hline(
            y=0.7,
            line_dash="dash",
            line_color="yellow",
            annotation_text="MONITORING",
        )
        fig.add_hline(
            y=0.3, line_dash="dash", line_color="orange", annotation_text="TRANSMUTING"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Time",
            yaxis_title="T_D Index",
            yaxis=dict(range=[0, 1.05]),
            hovermode="x unified",
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
        )
    else:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            annotations=[
                {
                    "text": "Waiting for data...",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20},
                }
            ],
        )

    return kpi_td, kpi_supernova, table_rows, stream_matrix, fig, td_history


# === Main Entry Point ===

if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=8050,
    )
