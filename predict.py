import re
import pandas as pd
import joblib

model = joblib.load("model/password_risk_model.pkl")
common_words = {"password","admin","welcome","hello","india","love","qwerty","letmein"}

def extract_features(password):
    return {
        "length": len(password),
        "has_digit": int(bool(re.search(r"\d", password))),
        "has_symbol": int(bool(re.search(r"\W", password))),
        "has_upper": int(bool(re.search(r"[A-Z]", password))),
        "has_lower": int(bool(re.search(r"[a-z]", password))),
        "digit_count": len(re.findall(r"\d", password)),
        "symbol_count": len(re.findall(r"\W", password)),
        "upper_count": len(re.findall(r"[A-Z]", password)),
        "lower_count": len(re.findall(r"[a-z]", password)),
        "has_common_word": int(any(w in password.lower() for w in common_words)),
    }

while True:
    pwd = input("Enter a password (or 'exit' to quit): ")
    if pwd.lower() == "exit":
        break
    features = pd.DataFrame([extract_features(pwd)])
    prediction = model.predict(features)[0]
    label = "Weak" if prediction == 1 else "Strong"
    print(f"Password: {pwd} → {label}")
