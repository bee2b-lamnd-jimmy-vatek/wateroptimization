import dash
from dash import  html
import pandas as pd
import io, base64
import dash_bootstrap_components as dbc
from callbacks import init_callbacks
from components.data_input_section import data_input_section
from components.features_section import features_section
from components.bounds_rules_section import bounds_rules_section
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div("Name", className="title"),
    html.Div([   
        dbc.Col([data_input_section], className="card-box"),
        dbc.Col([features_section],className="card-box"),
        dbc.Col([bounds_rules_section],className="card-box"),
    ], style={"display": "flex","flex-direction": "column","gap": "20px" } , className="mt-4 mx-5"),
], className="")

init_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)
