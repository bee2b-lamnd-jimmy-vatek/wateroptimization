import numpy as np
import optuna
import joblib
import pandas as pd
import warnings
from tensorflow import keras
warnings.filterwarnings("ignore", category=UserWarning)

# Load NN model, scaler, and encoder (from autoencoder)
model = keras.models.load_model("quality_predictor_bnnlite.keras")
scaler = joblib.load("scaler.pkl")
encoder = keras.models.load_model("encoder_model.keras")

# 4 controllable variables
controllable_cols = ["agitator_speed", "coolant_flow", "residence_time", "feed_temp"]

# bounds (adjust according to actual data range)
bounds = [
    (200, 400),   # agitator_speed
    (80, 120),    # coolant_flow
    (30, 60),     # residence_time
    (40, 70)      # feed_temp
]

def objective(trial):
    # sample values from bounds
    x_c = [trial.suggest_float(col, lo, hi) for (col, (lo, hi)) in zip(controllable_cols, bounds)]
    full_df = pd.DataFrame([x_c], columns=controllable_cols)
    full_scaled = scaler.transform(full_df)
    full_latent = encoder.predict(full_scaled)
    pred = model.predict(full_latent, verbose=0)[0][0]
    return -pred   # maximize quality → minimize negative

def optimize_global(n_trials=200, custom_bounds=None):
    default_bounds = [
        (200, 400), 
        (80, 120),  
        (30, 60),     
        (40, 70)     
    ]
    bounds = []
    for i, col in enumerate(controllable_cols):
        if custom_bounds and col in custom_bounds and custom_bounds[col] is not None:
            bounds.append(custom_bounds[col])
        else:
            bounds.append(default_bounds[i])

    def objective(trial):
        x_c = [trial.suggest_float(col, lo, hi) for (col, (lo, hi)) in zip(controllable_cols, bounds)]
        full_df = pd.DataFrame([x_c], columns=controllable_cols)
        full_scaled = scaler.transform(full_df)
        full_latent = encoder.predict(full_scaled)
        pred = model.predict(full_latent, verbose=0)[0][0]
        return -pred

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)

    best_x = {col: study.best_params[col] for col in controllable_cols}
    best_quality = -study.best_value
    return best_x, best_quality