from dash import html

context_section = html.Div([
    html.Div("Context for optimization", className="section-title"),
    html.Div("Context variables (non-controllable) will be held fixed at these values during optimization.", className="label"),
])