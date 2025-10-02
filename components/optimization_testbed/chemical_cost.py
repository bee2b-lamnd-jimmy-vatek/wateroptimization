from dash import html, dcc
import dash_bootstrap_components as dbc

chemical_cost = html.Div([
        html.Div("Chemical Cost", className="section-title"),
        dbc.Row([
            dbc.Col([
                html.Div("Citric Acid 50 percent dollars per L", className="label"),
                dcc.Input(type="number", placeholder="e.g. 3.2", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
            dbc.Col([
                html.Div("Hypo Chlorite 12.5 percent dollars per L", className="label"),
            dcc.Input(type="number", placeholder="e.g. 0.4", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
        ],className="g-2"),
   
])  