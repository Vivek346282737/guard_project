from flask import Flask, request, render_template
import joblib, re, pandas as pd

app = Flask(__name__)
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
    score += min(len(p), 20) * 2
    score += 10 if re.search(r"[A-Z]", p) else 0
    score += 10 if re.search(r"[a-z]", p) else 0
    score += 10 if re.search(r"\d", p) else 0
    score += 20 if re.search(r"\W", p) else 0
    score -= 20 if any(w in p.lower() for w in common_words) else 0
    return max(0, min(100, score))

def tips(p):
    out = []
    if len(p) < 12: out.append("Increase length to 12+")
    if not re.search(r"[A-Z]", p): out.append("Add uppercase")
    if not re.search(r"[a-z]", p): out.append("Add lowercase")
    if not re.search(r"\d", p): out.append("Include a digit")
    if not re.search(r"\W", p): out.append("Add a special character")
    if any(w in p.lower() for w in common_words): out.append("Avoid common words")
    return out

@app.route("/", methods=["GET", "POST"])
def index():
    result, password, score, suggestions = None, "", None, []
    if request.method == "POST":
        password = request.form["password"]
        features = pd.DataFrame([extract_features(password)])
        prediction = model.predict(features)[0]
        result = "Weak" if prediction == 1 else "Strong"
        score = heuristics_score(password)
        suggestions = tips(password)
    return render_template("index.html", result=result, password=password, score=score, suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)
