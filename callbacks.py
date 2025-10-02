from dash import Input, Output, State, html, dcc, dash_table, MATCH
import dash
import pandas as pd, io, base64
import json
import dash_bootstrap_components as dbc
from components.manual_section import manual_section  
from optimization import optimize_global
from train_model import train_with_df
from predict_model import predict_quality
import base64
import io
import pandas as pd
from dash.dependencies import Input, Output, State

ramp_plan = [
    {"mv": "agitator_speed", "current": 200, "target": 350, "max_step": 10, "steps": 15, "path": [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350]},
    # Thêm các biến khác nếu muốn
]
drivers = [
    {"feature": "agitator_speed", "importance": 0.45},
    {"feature": "coolant_flow", "importance": 0.35},
    {"feature": "residence_time", "importance": 0.15},
    {"feature": "feed_temp", "importance": 0.05},
]
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df
    return None

def init_callbacks(app):
    @app.callback(
        [Output("preview-table", "data"),
         Output("preview-table", "columns"),
         Output("dropdown-cols", "options"),
         Output("dropdown-target", "options"),
         Output("dropdown-target", "value")],
        [Input("upload-data", "contents"),
         Input("dropdown-target", "value")],
        State("upload-data", "filename")
    )
    def update_table(contents, target, filename):
        if contents is None:
            return [], [], [], [], None

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        df = df.round(4)

        if target is None or target not in df.columns:
            target = df.columns[-1]

        target_options = [{"label": col, "value": col} for col in df.columns]
       
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        feature_options = [
            {"label": col, "value": col}
            for col in numeric_cols if col != target
        ]

        return (
            df.head().to_dict("records"),
            [{"name": i, "id": i} for i in df.columns],
            feature_options,
            target_options,
            target
        )
    
    @app.callback(
        [Output("train-metrics", "children"),
        Output("test-metrics", "children"),
        Output("dist-metrics", "children")],
        Input("dropdown-target", "value") 
    )
    def update_metrics(target):
        train = {"R2": 0.96, "MAE": 0.75, "RMSE": 0.92}
        test = {"R2": 0.83, "MAE": 1.75, "RMSE": 2.22, "Pred SD (median)": 0.116}
        dist = {
            "Mahalanobis (train median)": 1.94,
            "Mahalanobis (test median)": 1.94,
            "Mahalanobis (test 95th pct)": 2.60
        }
        return json.dumps(train, indent=4), json.dumps(test, indent=4), json.dumps(dist, indent=4)


    @app.callback(
        Output("bounds-container", "children"),
        Input("dropdown-cols", "value"),
        Input("default-bounds", "value"),  
        State("upload-data", "contents"),
        prevent_initial_call=True
    )
    def update_bounds_inputs(selected_cols, default_bounds, contents):
        if not selected_cols or contents is None:
            return html.Div("No controllable variables selected.")

        import io, base64, pandas as pd
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        inputs = []
        for col in selected_cols:
            if default_bounds == "minmax":
                lower_val = df[col].min()
                upper_val = df[col].max()
            else:  # percentile
                lower_val = df[col].quantile(0.05)
                upper_val = df[col].quantile(0.95)

            lower_val = round(lower_val, 6)
            upper_val = round(upper_val, 6)

            inputs.append(
                html.Div([
                    html.Div(f"{col} lower bound", className="label"),
                    dcc.Input(
                        id={"type": "bound-input", "col": col, "bound": "lower"},
                        type="number", step="any", value=lower_val,
                        style={"width": "100%", "marginBottom": "10px"},className="my-dropdown"
                    ),
                    html.Div(f"{col} upper bound", className="label"),
                    dcc.Input(
                        id={"type": "bound-input", "col": col, "bound": "upper"},
                        type="number", step="any", value=upper_val,
                        style={"width": "100%", "marginBottom": "20px"},className="my-dropdown"
                    ),
                ])
            )
        return inputs
    
    @app.callback(
        Output("modal-optimize", "is_open"),
        Output("optimization-result", "children"),
        Input("btn-optimize", "n_clicks"),
        Input("close-optimize", "n_clicks"),
        State("modal-optimize", "is_open"),
        prevent_initial_call=True
    )
    def toggle_modal(open_click, close_click, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            return is_open, ""

        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger == "btn-optimize":
            best_x, best_quality = optimize_global(n_trials=200)
            # Tạo layout kết quả từ best_x, best_quality
            result_layout = html.Div([
                html.H4("Recommended setpoint"),
                html.Pre(json.dumps({
                    "setpoints": best_x,
                    "expected_target_mean": best_quality
                }, indent=4)),

                html.H4("Ramp plan (rate-limited moves)"),
                html.Pre(json.dumps(ramp_plan, indent=4)),

                html.H4("Local drivers at recommended setpoint"),
                dash_table.DataTable(
                    id="drivers-table",
                    columns=[{"name": i, "id": i} for i in ["feature", "importance"]],
                    data=drivers,
                    style_table={"overflowX": "auto"},
                    style_cell={"padding": "5px", "textAlign": "left"},
                    style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
                ),

                html.Br(),
                html.Div([
                    dbc.Button("⬇ Download JSON", id="btn-download", color="primary", n_clicks=0),
                    dcc.Download(id="download-json")
                ]),

                html.Br(),
                 dbc.Col([manual_section], className="card-box"), 
            ])

            return True, result_layout

        elif trigger == "close-optimize":
            return False, ""
        return is_open, ""

    @app.callback(
        Output('train-result', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def train_callback(contents, filename):
        if contents:
            df = parse_contents(contents, filename)
            result = train_with_df(df)
            return f"MAE: {result['mae']:.3f}, RMSE: {result['rmse']:.3f}, R2: {result['r2']:.3f}"
        return ""

    @app.callback(
        Output('predict-result', 'children'),
        Input('btn-predict', 'n_clicks'),
        State('input-agitator-speed', 'value'),
        State('input-coolant-flow', 'value'),
        State('input-residence-time', 'value'),
        State('input-feed-temp', 'value'),
        prevent_initial_call=True
    )
    def manual_predict(n_clicks, agitator_speed, coolant_flow, residence_time, feed_temp):
        if n_clicks and None not in (agitator_speed, coolant_flow, residence_time, feed_temp):
            result = predict_quality(agitator_speed, coolant_flow, residence_time, feed_temp)
            return f"Prediction: {result['mean_prediction']:.3f} ± {result['uncertainty']:.3f}"
        return ""
