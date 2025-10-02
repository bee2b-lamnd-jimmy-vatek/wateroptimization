from dash import html, dcc
import dash_bootstrap_components as dbc


baseline_info = html.Div([
    html.Div("Baseline Info", className="section-title"),   
    dbc.Row([
        dbc.Col([
            html.Div("Start Time", className="label"),
            dcc.Input(type="text", placeholder="YYYY-MM-DD HH:MM:SS", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("End Time", className="label"),
            dcc.Input(type="text", placeholder="YYYY-MM-DD HH:MM:SS", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Net Water Production per day", className="label"),
            dcc.Input(type="number", placeholder="533.33", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Total Cost per day", className="label"),
            dcc.Input(type="number", placeholder="67.29", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),
        dbc.Col([
            html.Div("Number of Hypo MCs per 7 days", className="label"),
            dcc.Input(type="number", placeholder="6", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Avg Hypo dosage per cleaning", className="label"),
            dcc.Input(type="number", placeholder="612", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Number of CA MCs per 7 days", className="label"),
            dcc.Input(type="number", placeholder="1", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Avg CA dosage per cleaning", className="label"),
            dcc.Input(type="number", placeholder="1400", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),
        dbc.Col([
            html.Div("Permeability loss in percent", className="label"),
            dcc.Input(type="number", placeholder="19", 
                      className="my-dropdown", style={"width": "80%"})
        ], width=3),
    ], className="g-2 mt-2"),
])
