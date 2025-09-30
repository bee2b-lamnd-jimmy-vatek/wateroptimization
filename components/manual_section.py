from dash import dcc, html
import dash_bootstrap_components as dbc

manual_section = html.Div([
    html.Div("Manual What-if Sandbox",className="section-title"),

    html.Div("agitator_speed", className="label"),
    dcc.Slider(
        id="agitator_speed_result", min=212.26, max=392.65, step=0.01, value=301.67,
        marks={212.26: "212.26", 392.65: "392.65"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Div("coolant_flow", className="label"),
    dcc.Slider(
        id="coolant_flow_result", min=82.34, max=117.64, step=0.01, value=105.72,
        marks={82.34: "82.34", 117.64: "117.64"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Br(),
    html.Div("residence_time", className="label"),
    dcc.Slider(
        id="residence_time_result", min=31.17, max=57.56, step=0.01, value=53.72,
        marks={31.17: "31.17", 357.56: "357.56"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Br(),
    html.Div("feed_temp", className="label"),
    dcc.Slider(
        id="feed_temp_result", min=41.36, max=68.65, step=0.01, value=44.97,
        marks={41.36: "41.36", 68.65: "68.65"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    dbc.Collapse(
        html.Pre(
            id={"type": "collapse-whatif", "index": 0},
            children='{\n  "Predicted KPI": 46.94,\n  "Uncertainty (SD)": 0.1274,\n  "Δ vs baseline": 0\n}',
            style={
                "whiteSpace": "pre-wrap",
                "wordBreak": "break-word",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "5px"
            }
        ),
        id="collapse-whatif",
        is_open=False
    ),
    

    html.Pre(
        id="whatif-json",
        children='{\n  "Predicted KPI": 46.94,\n  "Uncertainty (SD)": 0.1274,\n  "Δ vs baseline": 0\n}',
        style={
            "whiteSpace": "pre-wrap",
            "wordBreak": "break-word",
            "backgroundColor": "#f8f9fa",
            "padding": "10px",
            "borderRadius": "5px"
        }
    ),

    # --- Bullet points ---
    html.Ul([
        html.Li(html.Span([
            html.B("agitator_speed"), " is a strong driver around this point. Small adjustments here have a notable impact on the KPI."
        ])),
        html.Li(html.Span([
            html.B("feed_temp"), " is a strong driver around this point. Small adjustments here have a notable impact on the KPI."
        ])),
        html.Li(html.Span([
            html.B("coolant_flow"), " is a strong driver around this point. Small adjustments here have a notable impact on the KPI."
        ])),
    ]),

    # --- Notes ---
    html.P("MVP notes: • RandomForest ensemble uncertainty • Evolutionary optimizer • Mahalanobis distance to train • PDP-like what-ifs • No nested expanders",
           style={"fontSize": "0.7rem", "color": "gray"})
])