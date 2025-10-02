from dash import html, dcc
import dash_bootstrap_components as dbc

update_csv = html.Div([
    html.Div("Upload a CSV file", className="section-title"),
    dcc.Upload(
        id="upload-data",
        children=html.Div(["Drag & Drop or ", html.A("Browse Files")]),
        className="upload-area",
        style={
            "width": "100%", "height": "60px", "lineHeight": "60px",
            "borderRadius": "5px", "textAlign": "center"
        }
    ),
    dbc.Row([
        dbc.Col([
            html.Div("turbidity", className="label"),
            dcc.Input(type="text", placeholder="e.g. turbidity", className="my-dropdown",style={"width": "80%"} )
        ], width=3),
        dbc.Col([
            html.Div("flux", className="label"),
            dcc.Input(type="text", placeholder="e.g. flux", className="my-dropdown", style={"width": "80%"} )
        ], width=3),

        dbc.Col([
            html.Div("perm", className="label"),
            dcc.Input(type="text", placeholder="e.g. perm", className="my-dropdown", style={"width": "80%"} )
        ], width=3),

        dbc.Col([
            html.Div("tmp", className="label"),
            dcc.Input(type="text", placeholder="e.g. tmp", className="my-dropdown", style={"width": "80%"} )
        ], width=3),
        dbc.Col([
            html.Div("UF2 Filtrate pump valve status", className="label"),
            dcc.Input(type="text", placeholder="e.g. UF2 Filtrate pump valve status", className="my-dropdown", style={"width": "80%"} )
        ], width=3),

        dbc.Col([
            html.Div("UF2 Drain valve status", className="label"),
            dcc.Input(type="text", placeholder="e.g. UF2 Drain valve status", className="my-dropdown", style={"width": "80%"} )
        ], width=3),

        dbc.Col([
            html.Div("Hypo dosing pump flow rate", className="label"),
            dcc.Input(type="text", placeholder="e.g. Hypo dosing pump flow rate", className="my-dropdown", style={"width": "80%"} )
        ], width=3),

        dbc.Col([
            html.Div("CA dosing pump flow rate", className="label"),
            dcc.Input(type="text", placeholder="e.g. CA dosing pump flow rate", className="my-dropdown", style={"width": "80%"} )
        ], width=3),
        ],className="g-2 mt-2"),
        
])