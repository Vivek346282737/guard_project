import re, pandas as pd, joblib

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

def heuristics_score(p):
    score = 0
    score += min(len(p), 20) * 2            # length up to 40 pts
    score += 10 if re.search(r"[A-Z]", p) else 0
    score += 10 if re.search(r"[a-z]", p) else 0
    score += 10 if re.search(r"\d", p) else 0
    score += 20 if re.search(r"\W", p) else 0
    score -= 20 if any(w in p.lower() for w in common_words) else 0
    return max(0, min(100, score))

def suggestions(p):
    tips = []
    if len(p) < 12: tips.append("Increase length to 12+")
    if not re.search(r"[A-Z]", p): tips.append("Add at least 1 uppercase letter")
    if not re.search(r"[a-z]", p): tips.append("Add at least 1 lowercase letter")
    if not re.search(r"\d", p): tips.append("Include a digit")
    if not re.search(r"\W", p): tips.append("Add a special character (!@#$...)")
    if any(w in p.lower() for w in common_words): tips.append("Avoid common words (password, admin, qwerty)")
    return tips

while True:
    pwd = input("Enter a password (or 'exit' to quit): ")
    if pwd.lower() == "exit":
        break
    features = pd.DataFrame([extract_features(pwd)])
    prediction = model.predict(features)[0]
    label = "Weak" if prediction == 1 else "Strong"
    score = heuristics_score(pwd)
    tips = suggestions(pwd)
    print(f"Password: {pwd} → {label} (Score: {score}/100)")
    if tips:
        print("Improve by:", "; ".join(tips))
