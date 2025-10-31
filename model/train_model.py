import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import re
import os

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Dummy dataset (baad me breaches.csv use kar sakte ho)
df = pd.DataFrame({
    "password": ["123456", "password", "Vivek@2025", "Hello123!"],
    "exposed": [1, 1, 0, 0]
})

# Feature engineering
df["length"] = df["password"].apply(len)
df["has_digit"] = df["password"].str.contains(r"\d").astype(int)
df["has_symbol"] = df["password"].str.contains(r"\W").astype(int)

X = df[["length", "has_digit", "has_symbol"]]
y = df["exposed"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model/password_risk_model.pkl")
print("✅ Model trained and saved as model/password_risk_model.pkl")
