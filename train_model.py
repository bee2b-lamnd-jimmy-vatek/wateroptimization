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
    latent_dim = 4  # Tăng latent_dim từ 2 lên 4

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
        epochs=300,               
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

    # 11. Monte Carlo Dropout inference (for uncertainty estimation)
    sample = np.array([[394.33983929854327, 80.01656463304573, 56.18025153633774, 69.97894198886914]])  # Best controllable settings
    sample_scaled = scaler.transform(sample)
    sample_latent = encoder.predict(sample_scaled)

    results = []
    for _ in range(50):
        pred = model(sample_latent, training=True).numpy()[0][0]
        results.append(pred)

    mean_pred = np.mean(results)
    std_pred = np.std(results)

    print("\n50 MC Dropout predictions:")
    print(results)
    print(f"Mean prediction: {mean_pred:.3f}")
    print(f"Std deviation (uncertainty): {std_pred:.3f}")
    print(f"Max difference: {max(results)-min(results):.6f}")

    # 12. Build decoder separately
    encoded_inputs = keras.Input(shape=(latent_dim,))
    x = layers.Dense(8, activation='relu')(encoded_inputs)
    decoded_outputs = layers.Dense(input_dim, activation='linear')(x)
    decoder = keras.Model(encoded_inputs, decoded_outputs)

    # 13. Decode latent back to original controllables
    decoded_scaled = decoder.predict(sample_latent)  
    decoded_original = scaler.inverse_transform(decoded_scaled)  

    print("Decoded controllables from latent (scaled):", decoded_scaled)
    print("Decoded controllables (real values):", decoded_original)

    return {"mae": test_mae, "rmse": rmse_test, "r2": r2_test}
