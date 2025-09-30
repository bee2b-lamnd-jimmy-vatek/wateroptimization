from dash import Input, Output, State, html, dcc, dash_table
import dash
import pandas as pd, io, base64
import json
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
            recommended_setpoint = {
                "setpoints": {
                    "agigator_speed": 248.27,
                    "coolant_flow": 117.63,
                    "residence_time": 54.93,
                    "feed_temp": 41.74,
                },
                "expected_target_mean": 39.69,
                "predicted_sigma": 0.103,
                "risk_adjusted_objective": 39.72,
                "distance_to_training (Mahalanobis)": 2.59,
                "goal": "Maximize",
                "lambda_uncertainty": 0.3
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
                )
            ])

            return True, result_layout

        elif trigger == "close-optimize":
            return False, ""

        return is_open, ""