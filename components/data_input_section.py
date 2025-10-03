from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
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
    dcc.Loading(
        id="loading-table",
        type="circle", 
        children=dash_table.DataTable(
            id="preview-table",
            style_table={"overflowX": "auto"},
        ),
        fullscreen=False  
    ),
])
