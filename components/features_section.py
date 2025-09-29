from dash import dcc, html
import dash_bootstrap_components as dbc
features_section = html.Div([
    html.Div("Choose target & features", className="section-title"),

    html.Div("Select KPI/Objective (target variable)", className="label"),
    dcc.Dropdown(id="dropdown-target", placeholder="Select..."),
    html.Br(),

    html.Div("Controllable (MVs) to optimize", className="label"),
    dcc.Dropdown(id="dropdown-cols", multi=True, placeholder="Select...."),
    html.Br(),

    html.Div("Context variables (fixed during optimization)", className="label"),
    dcc.Slider(
        id="Context-variables", min=3, max=20, step=1, value=7,
        marks={3: "3", 20: "20"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Br(),

    html.Div("Trees per model", className="label"),
    dcc.Slider(
        id="trees-per-model", min=100, max=600, step=1, value=300,
        marks={100: "100", 600: "600"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Br(),

    html.Div("Max tree depth (None = unlimited)", className="label"),
    dcc.Dropdown(['None'], 'None', id="dropdown-depth", placeholder="Select..."),
    html.Br(),

    # === Metrics & results ===
    html.Hr(),
    dbc.Row([
    dbc.Col([
        html.Div("Train metrics", className="section-title"),
        html.Pre(id="train-metrics", style={"backgroundColor": "#f9f9f9", "padding": "10px","margin-bottom": "0px"})
    ], width=4),

    dbc.Col([
        html.Div("Test metrics", className="section-title"),
        html.Pre(id="test-metrics", style={"backgroundColor": "#f9f9f9", "padding": "10px","margin-bottom": "0px"})
    ], width=4),

    dbc.Col([
        html.Div("Distribution & safety checks", className="section-title"),
        html.Pre(id="dist-metrics", style={"backgroundColor": "#f9f9f9", "padding": "10px","margin-bottom": "0px"})
    ], width=4),
], className="mt-3")
])
