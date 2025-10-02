from dash import html, dcc
import dash_bootstrap_components as dbc

membrane_info = html.Div([
    html.Div("Membrane Info", className="section-title"),
    html.Div("Membrane Type", className="label"),
    dcc.RadioItems(
        id="membrane-type",
        options=[
            {"label": "UF Membrane", "value": "UF"},
            {"label": "RO Membrane", "value": "RO"},
        ],
        value="UF",
        inline=True, 
        inputClassName="radio-btn", 
        labelClassName="radio-label"
    )

])