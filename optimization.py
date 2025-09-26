import numpy as np
import optuna
import joblib
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# load pretrained model + scaler
model = joblib.load("surrogate_lgbm.pkl")
scaler = joblib.load("scaler.pkl")

controllable_cols = ["feed_temp", "residence_time"]
non_controllable_cols = ["agitator_speed", "coolant_flow"]

# controllable bounds (match your process)
bounds = [(0, 10), (0, 5)]  

def global_objective(x_c, X_nc):
    qualities = []
    for x_nc in X_nc:
        full_input = np.concatenate([x_c, x_nc])
        full_df = pd.DataFrame([full_input], columns=controllable_cols + non_controllable_cols)
        full_scaled = scaler.transform(full_df)
        qualities.append(model.predict(full_scaled)[0])
    return np.mean(qualities)

def optimize_global(df, n_trials=100):
    X_nc = df[non_controllable_cols].values.astype(float)

    def obj(trial):
        x_c = [trial.suggest_float(f"c{i}", lo, hi) for i, (lo, hi) in enumerate(bounds)]
        return -global_objective(np.array(x_c), X_nc)  # negate for minimization

    study = optuna.create_study(direction="minimize")
    study.optimize(obj, n_trials=n_trials)

    best_x = [study.best_params[f"c{i}"] for i in range(len(bounds))]
    best_quality = -study.best_value
    return dict(zip(controllable_cols, best_x)), best_quality

uploaded_df = pd.read_csv("uploaded.csv")

best_x, best_quality = optimize_global(uploaded_df, n_trials=200)

print("✅ Best controllable settings:", best_x)
print("✅ Predicted global quality:", best_quality)
