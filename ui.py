import dash
from dash import  html
import pandas as pd
import dash_bootstrap_components as dbc
from callbacks import init_callbacks
from components.data_input_section import data_input_section
from components.features_section import features_section
from components.bounds_rules_section import bounds_rules_section
from components.context_section import context_section
from components.optimization_section import optimization_section
from components.optimization_modal import optimization_modal
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div("Water optimization", className="title"),
    html.Div([   
        dbc.Col([data_input_section], className="card-box"),
        dbc.Col([features_section],className="card-box"),
        dbc.Col([bounds_rules_section],className="card-box"),
        dbc.Col([context_section],className="card-box"),
        dbc.Col([optimization_section],className="card-box"),   
        optimization_modal,
    ], style={"display": "flex","flex-direction": "column","gap": "20px" } , className="mt-4 mx-5"),
], className="")

init_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)
