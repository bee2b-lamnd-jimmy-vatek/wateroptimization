from dash import dcc, html
import dash_bootstrap_components as dbc


bounds_rules_section = html.Div([
    html.Div("Set bounds & rules", className="section-title"),

    html.Div("Default bounds", className="label"),
    dcc.RadioItems(
        id="default-bounds",
        options=[
            {"label": "Min/Max (observed)", "value": "minmax"},
            {"label": "5th - 95th percentile", "value": "percentile"},
        ],
        value="percentile",
        labelStyle={"display": "inline-block", "marginRight": "15px"},
    ),
    html.Br(),

    html.Div(id="bounds-container"),
])