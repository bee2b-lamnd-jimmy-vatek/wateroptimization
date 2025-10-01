import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- Trial Conditions Input ---
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

# --- Membrane Constants Section ---
membrane_constants = dbc.Accordion([
    dbc.AccordionItem([
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

    ], title="Membrane Constants"),
])

# --- Cost Per Unit ---
cost_per_unit = dbc.Accordion([
    dbc.AccordionItem([
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
    ],title="Cost Per Unit")
]) 
# --- Chemical Cost ---
chemical_cost = dbc.Accordion([
    dbc.AccordionItem([
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
    ],title="Chemical Cost")
])  


# --- App Layout ---
app.layout = html.Div([
    html.Div("Optimization Testbed", className="title" ),
    html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="membrane-dropdown",
                    options=[
                        {"label": "UF Membrane Train 2", "value": "train2"},
                        {"label": "UF Membrane Train 3", "value": "train3"},
                    ],
                    placeholder="Select Membrane Train",
                    clearable=False,
                    className="my-dropdown"
                ),width=4
            ),
        dbc.Col(dcc.Input(type="text", placeholder="Trial Name", className="my-dropdown"), width=4)
        ], className="mb-2"),
        
        dbc.Col([trial_conditions], className="card-box"),
        dbc.Col([membrane_constants], className="card-box",style={"padding": "0px"}), 
        dbc.Col([cost_per_unit], className="card-box",style={"padding": "0px"}), 
        dbc.Col([chemical_cost], className="card-box",style={"padding": "0px"}), 
        dbc.Col(dbc.Button("RUN SIMULATION", id="btn-run", className="btn-primary")),
        
    ],style={"display": "flex","flex-direction": "column","gap": "20px" }, className="mx-4 mt-3 mb-5"), 
])

if __name__ == "__main__":
    app.run(debug=True, port=8060)
