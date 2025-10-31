import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os
import re

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("passwords.csv")

# Feature engineering
df["length"] = df["password"].apply(len)
df["has_digit"] = df["password"].str.contains(r"\d").astype(int)
df["has_symbol"] = df["password"].str.contains(r"\W").astype(int)
df["has_upper"] = df["password"].str.contains(r"[A-Z]").astype(int)
df["has_lower"] = df["password"].str.contains(r"[a-z]").astype(int)
df["digit_count"] = df["password"].str.count(r"\d")
df["symbol_count"] = df["password"].str.count(r"\W")
df["upper_count"] = df["password"].str.count(r"[A-Z]")
df["lower_count"] = df["password"].str.count(r"[a-z]")

common_words = {"password","admin","welcome","hello","india","love","qwerty","letmein"}
df["has_common_word"] = df["password"].str.lower().apply(
    lambda p: int(any(w in p for w in common_words))
)

X = df[[
    "length","has_digit","has_symbol","has_upper","has_lower",
    "digit_count","symbol_count","upper_count","lower_count","has_common_word"
]]
y = df["exposed"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model/password_risk_model.pkl")
print("✔️ Model trained and saved as model/password_risk_model.pkl")