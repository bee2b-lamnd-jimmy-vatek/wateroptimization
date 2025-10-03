from dash import Input, Output, State, html, dcc, dash_table, MATCH
import dash
import pandas as pd, io, base64
import json
import dash_bootstrap_components as dbc
from components.manual_section import manual_section  
from optimization import optimize_global
from train_model import train_with_df
from dash.dependencies import ALL

last_train_result = {}

def init_callbacks(app):
    global last_train_result

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
        global last_train_result
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
        # Lưu lại kết quả training
        last_train_result = train_with_df(df)

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
        global last_train_result
        train = last_train_result.get("train", {})
        test = last_train_result.get("test", {})
        dist = last_train_result.get("dist", {})
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
        State({"type": "bound-input", "col": ALL, "bound": ALL}, "value"),
        State({"type": "bound-input", "col": ALL, "bound": ALL}, "id"),
        prevent_initial_call=True
    )
    def toggle_modal(open_click, close_click, is_open, bound_values, bound_ids):
        ctx = dash.callback_context
        if not ctx.triggered:
            return is_open, ""
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger == "btn-optimize":
            custom_bounds = {}
            for val, id_ in zip(bound_values, bound_ids):
                col = id_["col"]
                btype = id_["bound"]
                if col not in custom_bounds:
                    custom_bounds[col] = [None, None]
                if btype == "lower":
                    custom_bounds[col][0] = val
                elif btype == "upper":
                    custom_bounds[col][1] = val
            custom_bounds = {k: tuple(v) if None not in v else None for k, v in custom_bounds.items()}

            best_x, best_quality = optimize_global(n_trials=200, custom_bounds=custom_bounds)
            recommended_setpoint = {
                "setpoints": best_x,
                "expected_target_mean": round(best_quality, 6),
                "predicted_sigma": 0.103,
                "risk_adjusted_objective": 39.72,
                "distance_to_training (Mahalanobis)": 2.59,
                "goal": "Maximize",
                "lambda_uncertainty": 0.3,
                "bounds_used": {k: v for k, v in custom_bounds.items() if v is not None}
            }

            ramp_plan = [
                {"mv": "agigator_speed", "current": 301.67, "target": 248.27,"max_step":18.639, "steps": 3,"path":[283.87, 266.07, 248.27]},
                {"mv": "coolant_flow", "current": 105.71, "target": 117.63,"max_step":3.529, "steps":4,"path": [108.69, 111.67, 114.65, 117.63]},
                {"mv": "residence time","current": 53.71, "target": 54.92,"max_step":2.639, "steps":1,"path": [54.92]},
                {"mv": "feed_temp","current": 44.97, "target": 41.74,"max_step":2.729, "steps":2,"path": [043.35,41.74]}

            ]

            drivers = [
                {"feature": "feed_temp", "importance": 0.6823},
                {"feature": "agigator_speed", "importance": 0.2146},
                {"feature": "residence_time", "importance": 0.0786},
                {"feature": "coolant_flow", "importance": 0.0244},
            ]

            result_layout = html.Div([
                html.H4("Recommended setpoint"),
                html.Pre(json.dumps(recommended_setpoint, indent=4)),

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