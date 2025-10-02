import joblib
from tensorflow import keras
import numpy as np

def predict_quality(agitator_speed, coolant_flow, residence_time, feed_temp):
    model = keras.models.load_model("quality_predictor_bnnlite.keras")
    scaler = joblib.load("scaler.pkl")
    encoder = keras.models.load_model("encoder_model.keras")

    sample = np.array([[agitator_speed, coolant_flow, residence_time, feed_temp]])
    sample_scaled = scaler.transform(sample)
    sample_latent = encoder.predict(sample_scaled)

    results = []
    for _ in range(50):
        pred = model(sample_latent, training=True).numpy()[0][0]
        results.append(pred)
    mean_pred = np.mean(results)
    std_pred = np.std(results)

    return {
        "mean_prediction": float(mean_pred),
        "uncertainty": float(std_pred),
        "all_predictions": [float(x) for x in results]
    }