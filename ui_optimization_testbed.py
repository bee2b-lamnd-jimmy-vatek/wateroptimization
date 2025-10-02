import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.optimization_testbed.trial_conditions import trial_conditions
from components.optimization_testbed.membrane_constants import membrane_constants
from components.optimization_testbed.cost_per_unit import cost_per_unit
from components.optimization_testbed.chemical_cost import chemical_cost
from components.uf_system_configuration.update_csv import update_csv
from components.uf_system_configuration.membrane_info import membrane_info
from components.uf_system_configuration.baseline_info import baseline_info


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


uf_system_config = html.Div([
    html.H5("UF System Configuration"),
    html.P("Here you can configure UF system parameters..."),
])

# --- App Layout ---
app.layout = html.Div([
    html.Div("Dashboard", className="title"),
    dcc.Tabs([
        dcc.Tab(label='Optimization Testbed', children=[
            html.Div([
                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id="membrane-dropdown",
                        options=[
                            {"label": "UF Membrane Train 2", "value": "train2"},
                            {"label": "UF Membrane Train 3", "value": "train3"},
                        ],
                        placeholder="Select Membrane Train",
                        clearable=False,
                        className="my-dropdown"
                    ), width=4),
                    dbc.Col(dcc.Input(type="text", placeholder="Trial Name", className="my-dropdown"), width=4)
                ], className="mb-2"),
                
                dbc.Col([trial_conditions], className="card-box"),
                dbc.Col([membrane_constants], className="card-box"), 
                dbc.Col([cost_per_unit], className="card-box"), 
                dbc.Col([chemical_cost], className="card-box"), 
                dbc.Col(dbc.Button("RUN SIMULATION", id="btn-run", className="btn-primary")),
            ], style={"display": "flex","flex-direction": "column","gap": "20px", "margin": "20px"}),
        ]),
        dcc.Tab(label='UF System Configuration', children=[
            html.Div([
                dbc.Row([
                    dbc.Col([
                    html.Div("Plant *", className="label"),
                    dcc.Input(type="text", placeholder="Sydney Watert", className="my-dropdown",style={"width": "80%"} )
                    ], width=3),
                    dbc.Col([
                    html.Div("Location", className="label"),
                    dcc.Input(type="text", placeholder="Sydney", className="my-dropdown",style={"width": "80%"})
                    ], width=3),

                    dbc.Col([
                    html.Div("Total Output", className="label"),
                    dcc.Input(type="number", placeholder="500", className="my-dropdown",style={"width": "80%"})
                    ], width=3),

                    dbc.Col([
                    html.Div("Site id", className="label"),
                    dcc.Input(type="text", placeholder="Site 1", className="my-dropdown",style={"width": "80%"})
                    ], width=3),
                ],className="g-2 mt-2"),
                dbc.Accordion([
                    dbc.AccordionItem(
                        children=[
                            dbc.Col([update_csv], className="card-box mt-3"),
                            dbc.Col([membrane_info], className="card-box mt-3"),
                            dbc.Col([baseline_info], className="card-box mt-3"),
                        ],
                        title=html.Div([
                            html.Span("UF Membrane Train 2", style={"flex": "1"}),
                            dbc.Button(
                            "🗑️",  
                            id="delete-train-2",
                            color="link",
                            style={
                                "padding": "0px",
                                "marginRight": "8px",
                                "fontSize": "18px",
                                "color": "red",
                            }
                        )
                        ],style={"display": "flex", "alignItems": "center", "justifyContent": "between", "width": "100%"}),  
                    )
                ], start_collapsed=False, className="card-box mt-3"),

                dbc.Accordion([
                                dbc.AccordionItem(
                                    children=[
                                        dbc.Col([update_csv], className="card-box mt-3"),
                                        dbc.Col([membrane_info], className="card-box mt-3"),
                                        dbc.Col([baseline_info], className="card-box mt-3"),
                                    ],
                                    title=html.Div([
                                        html.Span("UF Membrane Train 1", style={"flex": "1"}),
                                        dbc.Button(
                                        "🗑️",  
                                        id="delete-train-2",
                                        color="link",
                                        style={
                                            "padding": "0px",
                                            "marginRight": "8px",
                                            "fontSize": "18px",
                                            "color": "red",
                                        }
                                    )
                                    ],style={"display": "flex", "alignItems": "center", "justifyContent": "between", "width": "100%"}),  
                                )
                            ], start_collapsed=False, className="card-box mt-3")

            ],className="mx-4")
        ])
    ],className="custom-tabs")
])
if __name__ == "__main__":
    app.run(debug=True, port=8060)
