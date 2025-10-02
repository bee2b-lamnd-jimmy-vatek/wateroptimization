from dash import html, dcc
import dash_bootstrap_components as dbc

membrane_constants = html.Div([
        html.Div("Membrane Constants", className="section-title"),
        dbc.Row([
            dbc.Col([
                html.Div("Area in m²", className="label"),
                dcc.Input(type="number", placeholder="e.g. 10694.5", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
            dbc.Col([
                html.Div("MC Water Volume in m³", className="label"),
            dcc.Input(type="number", placeholder="e.g. 10", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
            dbc.Col([
                html.Div("MC Duration in min", className="label"),
                dcc.Input(type="number", placeholder="e.g. 60", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
            dbc.Col([
                html.Div("BW Water Volume in m³", className="label"),
                dcc.Input(type="number", placeholder="e.g. 1", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
            dbc.Col([
                html.Div("BW Duration in min", className="label"),
                dcc.Input(type="number", placeholder="e.g. 6", className="my-dropdown", style={"width": "80%"})
            ], width=3),

            dbc.Col([
                html.Div("Turbidity in NTU", className="label"),
                dcc.Input(type="number", placeholder="e.g. 0.47", className="my-dropdown", style={"width": "80%"})
            ], width=3),

            dbc.Col([
                html.Div("Permeability in L/m² per bar", className="label"),
                dcc.Input(type="number", placeholder="e.g. -170", className="my-dropdown", style={"width": "80%"})
            ], width=3),
        ], className="g-2"),
])