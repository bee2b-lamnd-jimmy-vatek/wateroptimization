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

    html.Div("Optional maximum change per move (% of span, used for ramp plan)", className="label"),
        dcc.Slider(
            id="max-change-per-move",
            min=0, max=50, step=0.1, value=10,
            marks={0: "0.00", 50: "50.00"},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    html.Br(),

        html.Div("Optimization goal", className="label"),
        dcc.RadioItems(
            id="optimization-goal",
            options=[
                {"label": "Minimize target", "value": "min"},
                {"label": "Maximize target", "value": "max"}
            ],
            value="max",
            labelStyle={"display": "inline-block", "marginRight": "15px"},
        ),

        html.Br(),

        html.Div("Risk aversion λ (penalize predictive uncertainty)", className="label"),
        dcc.Slider(
            id="risk-aversion",
            min=0, max=2, step=0.01, value=0.3,
            marks={0: "0.00", 2: "2.00"},
            tooltip={"placement": "bottom", "always_visible": True}
        )
])