# GUARD — Password Risk Analyzer 🔐

## 🚀 Overview
GUARD ek ML‑based password risk analyzer hai jo weak aur strong passwords detect karta hai aur user ko tips deta hai apna password strong banane ke liye.  
Ye project mera portfolio flagship hai jisme Machine Learning + Flask web app dono combine kiye gaye hain.

## 📂 Project Structure
- **train_model.py** → Model train aur save karta hai  
- **predict.py** → CLI me password check karne ka tool  
- **app.py** → Flask web app run karta hai  
- **templates/index.html** → Web UI (result, score bar, tips)  
- **passwords.csv** → Dataset  
- **requirements.txt** → Dependencies  

## ⚙️ Setup & Run
```bash
pip install -r requirements.txt
python train_model.py
python predict.py
python app.py
