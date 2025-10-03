import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import random
import tensorflow as tf
from scipy.spatial import distance

# Set random seed for reproducibility
seed = 42
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

def train_with_df(df):
    # 2. Split features (X) and target (y)
    X = df[["agitator_speed", "coolant_flow", "residence_time", "feed_temp"]]
    y = df["quality_index"]
    print(f"Original feature dimension: {X.shape[1]}")

    # 3. Scale data before autoencoder
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Train Autoencoder for nonlinear dimensionality reduction
    input_dim = X_scaled.shape[1]
    latent_dim = 4 

    inputs = keras.Input(shape=(input_dim,))
    encoded = layers.Dense(8, activation='relu')(inputs)
    encoded = layers.Dense(latent_dim, activation='relu')(encoded)
    decoded = layers.Dense(8, activation='relu')(encoded)
    decoded = layers.Dense(input_dim, activation='linear')(decoded)

    autoencoder = keras.Model(inputs, decoded)
    encoder = keras.Model(inputs, encoded)

    autoencoder.compile(optimizer='adam', loss='mse')
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    autoencoder.fit(
        X_scaled, X_scaled,
        epochs=100,                   
        batch_size=16,
        verbose=1,
        validation_split=0.2,
        callbacks=[early_stop]
    )

    # Encode data to latent space
    X_latent = encoder.predict(X_scaled)
    print(f"Reduced feature dimension (latent): {X_latent.shape[1]}")

    # 5. Split train/test in latent space
    X_train, X_test, y_train, y_test = train_test_split(X_latent, y, test_size=0.2)

    # 6. Build Bayesian-like Neural Network (MC Dropout) on latent space
    model = keras.Sequential([
    layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],), kernel_regularizer=keras.regularizers.l2(0.001)),  
    layers.Dropout(0.03),
    layers.Dense(32, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    layers.Dropout(0.02),
    layers.Dense(1)
    ])

    # 7. Compile
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])

    # 8. Train with early stopping
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = model.fit(X_train, y_train, epochs=100, batch_size=16,
                        validation_split=0.2, verbose=1, callbacks=[early_stop])

    # 9. Evaluate on test set
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    y_test_pred = model.predict(X_test, verbose=0).flatten()
    rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
    r2_test = r2_score(y_test, y_test_pred)
    print(f"Test MAE: {test_mae:.4f}")
    print(f"Test RMSE: {rmse_test:.4f}")
    print(f"Test R²: {r2_test:.4f}")

    # 10. Save model, scaler, and encoder
    model.save("quality_predictor_bnnlite.keras")
    joblib.dump(scaler, "scaler.pkl")
    encoder.save("encoder_model.keras")
    autoencoder.save("autoencoder_model.keras")

    print("BNN-lite model, scaler, and Autoencoder saved.")

    y_train_pred = model.predict(X_train, verbose=0).flatten()
    mae_train = mean_absolute_error(y_train, y_train_pred)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
    r2_train = r2_score(y_train, y_train_pred)
    train_metrics = {"R2": round(r2_train, 2), "MAE": round(mae_train, 2), "RMSE": round(rmse_train, 2)}
    print("Train metrics:", train_metrics)

    preds_mc = [model(X_test, training=True).numpy().flatten() for _ in range(50)]
    preds_mc = np.stack(preds_mc, axis=1)
    pred_sd = np.median(np.std(preds_mc, axis=1))
    print(f"Pred SD (median) on test set: {pred_sd:.3f}")

    mean_train = np.mean(X_train, axis=0)
    cov_train = np.cov(X_train, rowvar=False)
    inv_cov_train = np.linalg.pinv(cov_train)
    maha_train = [distance.mahalanobis(x, mean_train, inv_cov_train) for x in X_train]
    maha_test = [distance.mahalanobis(x, mean_train, inv_cov_train) for x in X_test]

    dist_metrics = {
        "Mahalanobis (train median)": round(np.median(maha_train), 2),
        "Mahalanobis (test median)": round(np.median(maha_test), 2),
        "Mahalanobis (test 95th pct)": round(np.percentile(maha_test, 95), 2)
    }
    print("Distribution & safety checks:", dist_metrics)

    return {
        "train": {
            "R2": round(r2_train, 2),
            "MAE": round(mae_train, 2),
            "RMSE": round(rmse_train, 2)
        },
        "test": {
            "R2": round(r2_test, 2),
            "MAE": round(test_mae, 2),
            "RMSE": round(rmse_test, 2),
            "Pred SD (median)": round(float(pred_sd), 3)
        },
        "dist": {
            "Mahalanobis (train median)": round(np.median(maha_train), 2),
            "Mahalanobis (test median)": round(np.median(maha_test), 2),
            "Mahalanobis (test 95th pct)": round(np.percentile(maha_test, 95), 2)
        }
    }
