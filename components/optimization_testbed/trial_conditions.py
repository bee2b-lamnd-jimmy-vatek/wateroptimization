from dash import html, dcc
import dash_bootstrap_components as dbc

trial_conditions = html.Div([
    html.Div("Trial Conditions", className="section-title"),
    dbc.Row([
        dbc.Col([
            html.Div("Average Flux in XX", className="label"),
            dcc.Input(type="number", placeholder="e.g. 42", className="my-dropdown",style={"width": "80%"} )
        ], width=3),
        dbc.Col([
            html.Div("Temperature °C", className="label"),
           dcc.Input(type="number", placeholder="e.g. 25", className="my-dropdown",style={"width": "80%"} )
        ], width=3),
        dbc.Col([
            html.Div("Max. allowable Permeability Drop L/M²/bar", className="label"),
            dcc.Input(type="number", placeholder="e.g. 50", className="my-dropdown",style={"width": "80%"} )
        ], width=3),
        dbc.Col([
            html.Div("Min. number of acid clean", className="label"),
            dcc.Input(type="number", placeholder="e.g. 1", className="my-dropdown",style={"width": "80%"} )
        ], width=3),
        dbc.Col([
            html.Div("Allowed MC intervals in hours", className="label"),
            dcc.Input(type="text", placeholder="e.g. [2,3]", className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Hypo Chemical Dosage in ppm", className="label"),
            dcc.Input(type="text", placeholder="e.g. [500,575,650,725]", className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("CA Chemical Dosage in ppm", className="label"),
            dcc.Input(type="text", placeholder="e.g. [1400]", className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Optimization Start Date", className="label"),
            dcc.Input(type="text", placeholder="e.g. 5/10/2023", className="my-dropdown", style={"width": "80%"})
        ], width=3),

        dbc.Col([
            html.Div("Time Horizon in days", className="label"),
            dcc.Input(type="number", placeholder="e.g. 12", className="my-dropdown", style={"width": "80%"})
        ], width=3),
    ],className="g-2"),
])