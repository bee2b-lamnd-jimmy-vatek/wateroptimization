from dash import dcc, html, dash_table

data_input_section = html.Div([
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
    html.Br(),
    html.Div("Test fraction (hold-out at the end of time)", className="label"),
    dcc.Slider(
        id="test-fraction", min=0.05, max=0.4, step=0.01, value=0.2,
        marks={0.05: "0.05", 0.4: "0.4"},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Br(),
    html.Div("Preview:", className="label"),
    dash_table.DataTable(
        id="preview-table",
        style_table={"overflowX": "auto"},
    ),
    html.Div(id="train-result", className="label", style={"marginTop": "10px"}),

    html.Hr(),
    html.Div("Manual Prediction", className="section-title"),
    html.Div([
        html.Div([
            html.Label("Agitator Speed"),
            dcc.Input(id="input-agitator-speed", type="number", placeholder="Agitator Speed", style={"width": "100%"}),
        ], style={"marginBottom": "10px"}),
        html.Div([
            html.Label("Coolant Flow"),
            dcc.Input(id="input-coolant-flow", type="number", placeholder="Coolant Flow", style={"width": "100%"}),
        ], style={"marginBottom": "10px"}),
        html.Div([
            html.Label("Residence Time"),
            dcc.Input(id="input-residence-time", type="number", placeholder="Residence Time", style={"width": "100%"}),
        ], style={"marginBottom": "10px"}),
        html.Div([
            html.Label("Feed Temp"),
            dcc.Input(id="input-feed-temp", type="number", placeholder="Feed Temp", style={"width": "100%"}),
        ], style={"marginBottom": "10px"}),
        html.Button("Predict", id="btn-predict", n_clicks=0, style={"marginTop": "10px"}),
        html.Div(id="predict-result", className="label", style={"marginTop": "10px"}),
    ], style={"maxWidth": "400px", "margin": "auto"}),
])
