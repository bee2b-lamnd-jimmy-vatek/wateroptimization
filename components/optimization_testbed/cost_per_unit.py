from dash import html, dcc
import dash_bootstrap_components as dbc

cost_per_unit = html.Div([
        html.Div("Cost Per Unit", className="section-title"),
        dbc.Row([
            dbc.Col([
                html.Div("Power Unit Cost in dollars per kWh", className="label"),
                dcc.Input(type="number", placeholder="e.g. 0.3", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
            dbc.Col([
                html.Div("Pump Efficiency in percent", className="label"),
            dcc.Input(type="number", placeholder="e.g. 60", className="my-dropdown",style={"width": "80%"} )
            ], width=3),
        ],className="g-2"),

])