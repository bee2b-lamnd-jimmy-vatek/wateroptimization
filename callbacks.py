from dash import Input, Output, State, html, dcc
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

        if target is None or target not in df.columns:
            target = df.columns[-1]

        target_options = [{"label": col, "value": col} for col in df.columns]
        feature_options = [{"label": col, "value": col} for col in df.columns if col != target]

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

        # đọc csv từ upload
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

            inputs.append(
                html.Div([
                    html.Div(f"{col} lower bound", className="label"),
                    dcc.Input(
                        id={"type": "bound-input", "col": col, "bound": "lower"},
                        type="number", step=0.01, value=lower_val,
                        style={"width": "100%", "marginBottom": "10px"}
                    ),
                    html.Div(f"{col} upper bound", className="label"),
                    dcc.Input(
                        id={"type": "bound-input", "col": col, "bound": "upper"},
                        type="number", step=0.01, value=upper_val,
                        style={"width": "100%", "marginBottom": "20px"}
                    ),
                ])
            )
        return inputs