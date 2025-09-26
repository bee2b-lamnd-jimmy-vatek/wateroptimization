import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMRegressor, early_stopping
import joblib

# ask if the controllable and non controllable is dynamic or not?

# load dataset
df = pd.read_csv("dummy_process_data_2.csv")

controllable_cols = ["feed_temp", "residence_time"]
non_controllable_cols = ["agitator_speed", "coolant_flow"]
target_col = "quality_index"

X = df[controllable_cols + non_controllable_cols]
y = df[target_col]

# scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# train model
model = LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=-1,
    num_leaves=31,
    random_state=42
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    eval_metric="rmse",
    callbacks=[early_stopping(stopping_rounds=50)]
)

# save model + scaler
joblib.dump(model, "surrogate_lgbm.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model trained and saved")
