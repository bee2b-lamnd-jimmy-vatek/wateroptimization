from dash import dcc, html
import dash_bootstrap_components as dbc

optimization_section = html.Div([
    html.Div("Optimization", className="section-title"),

    html.Div("Population size", className="label"),
    dcc.Slider(
        id="population-size",
        min=24, max=128, step=1, value=48,
        marks={24: "24", 128: "128"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
    html.Div("Generations", className="label"),
    dcc.Slider(
        id="generations",
        min=20, max=200, step=1, value=80,
        marks={20: "20", 200: "200"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Div("Mutation scale", className="label"),
    dcc.Slider(
        id="mutation-scale",
        min=0.02, max=0.5, step=0.01, value=0.15,
        marks={0.02: "0.02", 0.5: "0.50"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),    
    
    html.Div("Random seed", className="label"),
    dcc.Input(
        id={},
        type="number", step=1, value=0,
        style={"width": "100%", "marginBottom": "20px"}
    ),

    html.Br(),
    dbc.Button("Optimize now", id="btn-optimize", className="btn-primary"),
])