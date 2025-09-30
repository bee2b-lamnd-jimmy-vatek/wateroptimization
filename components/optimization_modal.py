from dash import html
import dash_bootstrap_components as dbc

optimization_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Optimization Result"),className="title"),
        dbc.ModalBody(
            html.Pre(
                id="optimization-result",
                style={
                    "whiteSpace": "pre-wrap",
                    "wordBreak": "break-word",
                    "backgroundColor": "#f8f9fa",
                    "padding": "10px",
                    "borderRadius": "5px"
                }
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-optimize", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal-optimize",
    is_open=False,
    size="lg",
    backdrop="static"
)
