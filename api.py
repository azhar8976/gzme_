# from fastapi import FastAPI
# import json
# from pathlib import Path
# import random
# import string
# from datetime import datetime

# app = FastAPI()

# DB = "database.json"

# def load():
#     if Path(DB).exists():
#         with open(DB) as f:
#             return json.load(f)
#     return []

# def save(data):
#     with open(DB, "w") as f:
#         json.dump(data, f, indent=4)

# def accno():
#     s = list(random.choices(string.ascii_uppercase, k=3) +
#              random.choices(string.digits, k=6))
#     random.shuffle(s)
#     return "".join(s)

# # ---------- Create ----------
# @app.post("/create")
# def create(name: str, email: str, phone: str, pin: str):
#     data = load()
#     acc = accno()

#     user = {
#         "name": name,
#         "email": email,
#         "phone": phone,
#         "pin": pin,
#         "account": acc,
#         "balance": 0,
#         "history": []
#     }

#     data.append(user)
#     save(data)

#     return {"msg": "created", "account": acc}

# # ---------- Login ----------
# @app.get("/login")
# def login(account: str, pin: str):
#     data = load()
#     for u in data:
#         if u["account"] == account and u["pin"] == pin:
#             return u
#     return {"error": "invalid"}

# # ---------- Deposit ----------
# @app.post("/deposit")
# def deposit(account: str, pin: str, amount: int):
#     data = load()
#     for u in data:
#         if u["account"] == account and u["pin"] == pin:
#             u["balance"] += amount
#             u["history"].append(f"{datetime.now()} +{amount}")
#             save(data)
#             return {"msg": "deposited"}
#     return {"error": "invalid"}

# # ---------- Withdraw ----------
# @app.post("/withdraw")
# def withdraw(account: str, pin: str, amount: int):
#     data = load()
#     for u in data:
#         if u["account"] == account and u["pin"] == pin:
#             if u["balance"] < amount:
#                 return {"error": "insufficient"}
#             u["balance"] -= amount
#             u["history"].append(f"{datetime.now()} -{amount}")
#             save(data)
#             return {"msg": "withdrawn"}
#     return {"error": "invalid"}

# # ---------- Details ----------
# @app.get("/details")
# def details(account: str, pin: str):
#     data = load()
#     for u in data:
#         if u["account"] == account and u["pin"] == pin:
#             return u
#     return {"error": "invalid"}

# # ---------- History ----------
# @app.get("/history")
# def history(account: str, pin: str):
#     data = load()
#     for u in data:
#         if u["account"] == account and u["pin"] == pin:
#             return u["history"]
#     return {"error": "invalid"}



from fastapi import FastAPI, HTTPException
import json
from pathlib import Path
import random
import string
from datetime import datetime

# ---------- APP ----------
app = FastAPI(
    title="AZZU BANK API",
    description="Welcome to Azzu Bank",
    version="1.0"
)

DB = "database.json"

# ---------- DB ----------
def load():
    if Path(DB).exists():
        with open(DB) as f:
            return json.load(f)
    return []

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

def accno():
    s = list(random.choices(string.ascii_uppercase, k=3) +
             random.choices(string.digits, k=6))
    random.shuffle(s)
    return "".join(s)

# ---------- HOME ----------
@app.get("/")
def home():
    return {
        "bank": "AZZU BANK",
        "message": "Welcome to Azzu Bank API",
        "docs": "/docs"
    }

# ---------- CREATE ----------
@app.post("/create")
def create(name: str, email: str, phone: str, pin: str):
    if len(pin) != 4:
        raise HTTPException(400, "PIN must be 4 digits")

    data = load()
    acc = accno()

    user = {
        "name": name,
        "email": email,
        "phone": phone,
        "pin": pin,
        "account": acc,
        "balance": 0,
        "history": []
    }

    data.append(user)
    save(data)

    return {"msg": "Account created", "account": acc}

# ---------- LOGIN ----------
@app.get("/login")
def login(account: str, pin: str):
    data = load()
    for u in data:
        if u["account"] == account and u["pin"] == pin:
            return {"msg": "Login success", "user": u}

    raise HTTPException(401, "Invalid account or PIN")

# ---------- DEPOSIT ----------
@app.post("/deposit")
def deposit(account: str, pin: str, amount: int):
    if amount <= 0:
        raise HTTPException(400, "Invalid amount")

    data = load()
    for u in data:
        if u["account"] == account and u["pin"] == pin:
            u["balance"] += amount
            u["history"].append(f"{datetime.now()} +{amount}")
            save(data)
            return {"msg": "Deposited", "balance": u["balance"]}

    raise HTTPException(401, "Invalid account or PIN")

# ---------- WITHDRAW ----------
@app.post("/withdraw")
def withdraw(account: str, pin: str, amount: int):
    if amount <= 0:
        raise HTTPException(400, "Invalid amount")

    data = load()
    for u in data:
        if u["account"] == account and u["pin"] == pin:
            if u["balance"] < amount:
                raise HTTPException(400, "Insufficient balance")

            u["balance"] -= amount
            u["history"].append(f"{datetime.now()} -{amount}")
            save(data)
            return {"msg": "Withdrawn", "balance": u["balance"]}

    raise HTTPException(401, "Invalid account or PIN")

# ---------- DETAILS ----------
@app.get("/details")
def details(account: str, pin: str):
    data = load()
    for u in data:
        if u["account"] == account and u["pin"] == pin:
            return u

    raise HTTPException(401, "Invalid account or PIN")

# ---------- HISTORY ----------
@app.get("/history")
def history(account: str, pin: str):
    data = load()
    for u in data:
        if u["account"] == account and u["pin"] == pin:
            return {"history": u["history"]}

    raise HTTPException(401, "Invalid account or PIN")