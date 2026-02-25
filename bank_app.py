# import streamlit as st
# from pathlib import Path
# import json
# import random
# import string
# import pandas as pd

# # -----------------------------
# # Config + Theme
# # -----------------------------
# st.set_page_config(
#     page_title="Azhar Bank",
#     page_icon="🏦",
#     layout="centered"
# )

# st.markdown("""
# <style>
# .card {
#     padding:20px;
#     border-radius:15px;
#     background:linear-gradient(135deg,#1f4cff,#00c6ff);
#     color:white;
#     box-shadow:0 4px 12px rgba(0,0,0,0.2);
# }
# .logo {
#     font-size:28px;
#     font-weight:bold;
#     color:#1f4cff;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="logo">🏦 AZHAR DIGITAL BANK</div>', unsafe_allow_html=True)
# st.divider()

# # -----------------------------
# # Backend
# # -----------------------------
# class Bank:
#     db = "bank.json"
#     users = []

#     if Path(db).exists():
#         with open(db) as f:
#             users = json.load(f)

#     @classmethod
#     def save(cls):
#         with open(cls.db, "w") as f:
#             json.dump(cls.users, f, indent=4)

#     @staticmethod
#     def gen_acc():
#         return "".join(random.choices(string.digits, k=10))

#     @staticmethod
#     def gen_upi(name):
#         return name.lower().replace(" ", "") + "@azhar"

#     @classmethod
#     def find(cls, acc, pin):
#         for u in cls.users:
#             if u["account"] == acc and u["pin"] == pin:
#                 return u
#         return None

#     @classmethod
#     def find_by_upi(cls, upi):
#         for u in cls.users:
#             if u["upi"] == upi:
#                 return u
#         return None


# # -----------------------------
# # Session
# # -----------------------------
# if "user" not in st.session_state:
#     st.session_state.user = None

# # -----------------------------
# # Menu
# # -----------------------------
# menu = st.selectbox(
#     "Menu",
#     ["Login", "Create Account", "Dashboard"]
# )

# # -----------------------------
# # Create
# # -----------------------------
# if menu == "Create Account":
#     st.subheader("Create Account")

#     name = st.text_input("Name")
#     phone = st.text_input("Phone")
#     pin = st.text_input("4 Digit PIN", type="password")

#     if st.button("Create"):
#         if len(pin) != 4:
#             st.error("PIN must be 4 digit")
#         else:
#             acc = Bank.gen_acc()
#             upi = Bank.gen_upi(name)

#             Bank.users.append({
#                 "name": name,
#                 "phone": phone,
#                 "pin": pin,
#                 "account": acc,
#                 "upi": upi,
#                 "balance": 0,
#                 "tx": []
#             })
#             Bank.save()
#             st.success("Account Created")
#             st.info(f"Account: {acc}")
#             st.info(f"UPI ID: {upi}")

# # -----------------------------
# # Login
# # -----------------------------
# elif menu == "Login":
#     st.subheader("Login")

#     acc = st.text_input("Account")
#     pin = st.text_input("PIN", type="password")

#     if st.button("Login"):
#         user = Bank.find(acc, pin)
#         if user:
#             st.session_state.user = user
#             st.success("Login success")
#         else:
#             st.error("Invalid")

# # -----------------------------
# # Dashboard
# # -----------------------------
# elif menu == "Dashboard":

#     user = st.session_state.user
#     if not user:
#         st.warning("Login first")
#         st.stop()

#     st.subheader(f"Welcome {user['name']}")

#     # Card UI
#     st.markdown(f"""
#     <div class="card">
#     <h3>{user['name']}</h3>
#     Account: {user['account']} <br>
#     UPI: {user['upi']} <br>
#     Balance: ₹{user['balance']}
#     </div>
#     """, unsafe_allow_html=True)

#     st.divider()

#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["Deposit/Withdraw", "UPI Transfer", "Change PIN", "History"]
#     )

#     # Deposit Withdraw
#     with tab1:
#         amt = st.number_input("Amount", min_value=1)

#         c1, c2 = st.columns(2)

#         if c1.button("Deposit"):
#             user["balance"] += amt
#             user["tx"].append({"type": "Deposit", "amount": amt})
#             Bank.save()
#             st.success("Deposited")

#         if c2.button("Withdraw"):
#             if user["balance"] >= amt:
#                 user["balance"] -= amt
#                 user["tx"].append({"type": "Withdraw", "amount": amt})
#                 Bank.save()
#                 st.success("Withdrawn")
#             else:
#                 st.error("Insufficient")

#     # UPI Transfer
#     with tab2:
#         upi = st.text_input("Receiver UPI")
#         amt = st.number_input("Amount ", min_value=1)

#         if st.button("Send"):
#             receiver = Bank.find_by_upi(upi)
#             if not receiver:
#                 st.error("UPI not found")
#             elif user["balance"] < amt:
#                 st.error("Insufficient")
#             else:
#                 user["balance"] -= amt
#                 receiver["balance"] += amt

#                 user["tx"].append(
#                     {"type": "UPI Sent", "amount": amt, "to": upi}
#                 )
#                 receiver["tx"].append(
#                     {"type": "UPI Received", "amount": amt, "from": user["upi"]}
#                 )

#                 Bank.save()
#                 st.success("UPI Transfer Success")

#     # Change PIN
#     with tab3:
#         old = st.text_input("Old PIN", type="password")
#         new = st.text_input("New PIN", type="password")

#         if st.button("Change PIN"):
#             if old == user["pin"] and len(new) == 4:
#                 user["pin"] = new
#                 Bank.save()
#                 st.success("PIN changed")
#             else:
#                 st.error("Invalid PIN")

#     # History
#     with tab4:
#         if user["tx"]:
#             df = pd.DataFrame(user["tx"])
#             st.dataframe(df)
#         else:
#             st.info("No transactions")



# import streamlit as st
# import json
# from pathlib import Path
# import random
# import string
# from datetime import datetime

# DB = "database.json"

# # ---------- DB ----------
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

# data = load()

# # ---------- Session ----------
# if "user" not in st.session_state:
#     st.session_state.user = None

# st.title("🏦 Bank Web App")

# menu = st.sidebar.selectbox(
#     "Menu",
#     ["Create", "Login", "Dashboard", "History", "Update", "PIN Change"]
# )

# # ---------- Create ----------
# if menu == "Create":
#     st.header("Create Account")

#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     phone = st.text_input("Phone")
#     pin = st.text_input("PIN", type="password")

#     if st.button("Create"):
#         acc = accno()
#         user = {
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "pin": pin,
#             "account": acc,
#             "balance": 0,
#             "history": []
#         }
#         data.append(user)
#         save(data)
#         st.success(f"Account created: {acc}")

# # ---------- Login ----------
# elif menu == "Login":
#     st.header("Login")

#     acc = st.text_input("Account")
#     pin = st.text_input("PIN", type="password")

#     if st.button("Login"):
#         for u in data:
#             if u["account"] == acc and u["pin"] == pin:
#                 st.session_state.user = u
#                 st.success("Login success")
#                 break
#         else:
#             st.error("Invalid")

# # ---------- Dashboard ----------
# elif menu == "Dashboard":
#     u = st.session_state.user
#     if not u:
#         st.warning("Login first")
#     else:
#         st.header("Dashboard")
#         st.write("Name:", u["name"])
#         st.write("Account:", u["account"])
#         st.write("Balance:", u["balance"])

#         col1, col2 = st.columns(2)

#         with col1:
#             amt = st.number_input("Deposit", 0)
#             if st.button("Deposit"):
#                 u["balance"] += amt
#                 u["history"].append(f"{datetime.now()} +{amt}")
#                 save(data)
#                 st.success("Deposited")

#         with col2:
#             amt2 = st.number_input("Withdraw", 0)
#             if st.button("Withdraw"):
#                 if u["balance"] >= amt2:
#                     u["balance"] -= amt2
#                     u["history"].append(f"{datetime.now()} -{amt2}")
#                     save(data)
#                     st.success("Withdrawn")
#                 else:
#                     st.error("Insufficient")

# # ---------- History ----------
# elif menu == "History":
#     u = st.session_state.user
#     if not u:
#         st.warning("Login first")
#     else:
#         st.header("Transaction History")
#         for h in u["history"]:
#             st.write(h)

# # ---------- Update ----------
# elif menu == "Update":
#     u = st.session_state.user
#     if not u:
#         st.warning("Login first")
#     else:
#         st.header("Update Details")
#         name = st.text_input("Name", u["name"])
#         email = st.text_input("Email", u["email"])
#         phone = st.text_input("Phone", u["phone"])

#         if st.button("Update"):
#             u["name"] = name
#             u["email"] = email
#             u["phone"] = phone
#             save(data)
#             st.success("Updated")

# # ---------- PIN ----------
# elif menu == "PIN Change":
#     u = st.session_state.user
#     if not u:
#         st.warning("Login first")
#     else:
#         st.header("Change PIN")
#         old = st.text_input("Old PIN", type="password")
#         new = st.text_input("New PIN", type="password")

#         if st.button("Change"):
#             if old == u["pin"]:
#                 u["pin"] = new
#                 save(data)
#                 st.success("PIN changed")
#             else:
#                 st.error("Wrong PIN")


import streamlit as st
import json
from pathlib import Path
import random
import string
from datetime import datetime

# ---------- STYLE ----------
st.set_page_config(page_title="Bank App", page_icon="🏦", layout="centered")

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.block-container {
    background: rgba(255,255,255,0.05);
    padding: 2rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f2027,#203a43);
}

button[kind="primary"] {
    background-color: #00c6ff;
    color: white;
    border-radius: 10px;
    border: none;
}

button {
    border-radius: 10px !important;
}

h1, h2, h3 {
    color: #00e5ff;
}

</style>
""", unsafe_allow_html=True)

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

data = load()

# ---------- Session ----------
if "user" not in st.session_state:
    st.session_state.user = None

st.title("🏦 Bank Web App")

menu = st.sidebar.selectbox(
    "Menu",
    ["Create", "Login", "Dashboard", "History", "Update", "PIN Change"]
)

# ---------- Create ----------
if menu == "Create":
    st.header("Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    pin = st.text_input("PIN", type="password")

    if st.button("Create"):
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
        st.success(f"Account created: {acc}")

# ---------- Login ----------
elif menu == "Login":
    st.header("Login")

    acc = st.text_input("Account")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        for u in data:
            if u["account"] == acc and u["pin"] == pin:
                st.session_state.user = u
                st.success("Login success")
                break
        else:
            st.error("Invalid")

# ---------- Dashboard ----------
elif menu == "Dashboard":
    u = st.session_state.user
    if not u:
        st.warning("Login first")
    else:
        st.header("Dashboard")

        # ----- BANK CARD -----
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg,#1f4037,#99f2c8);
        padding:20px;
        border-radius:15px;
        color:black;
        font-weight:bold;
        margin-bottom:20px;
        ">
        💳 ACCOUNT: {u["account"]} <br>
        👤 {u["name"]} <br>
        💰 BALANCE: ₹{u["balance"]}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            amt = st.number_input("Deposit", 0)
            if st.button("Deposit"):
                u["balance"] += amt
                u["history"].append(f"{datetime.now()} +{amt}")
                save(data)
                st.success("Deposited")

        with col2:
            amt2 = st.number_input("Withdraw", 0)
            if st.button("Withdraw"):
                if u["balance"] >= amt2:
                    u["balance"] -= amt2
                    u["history"].append(f"{datetime.now()} -{amt2}")
                    save(data)
                    st.success("Withdrawn")
                else:
                    st.error("Insufficient")

# ---------- History ----------
elif menu == "History":
    u = st.session_state.user
    if not u:
        st.warning("Login first")
    else:
        st.header("Transaction History")
        for h in u["history"]:
            st.write(h)

# ---------- Update ----------
elif menu == "Update":
    u = st.session_state.user
    if not u:
        st.warning("Login first")
    else:
        st.header("Update Details")
        name = st.text_input("Name", u["name"])
        email = st.text_input("Email", u["email"])
        phone = st.text_input("Phone", u["phone"])

        if st.button("Update"):
            u["name"] = name
            u["email"] = email
            u["phone"] = phone
            save(data)
            st.success("Updated")

# ---------- PIN ----------
elif menu == "PIN Change":
    u = st.session_state.user
    if not u:
        st.warning("Login first")
    else:
        st.header("Change PIN")
        old = st.text_input("Old PIN", type="password")
        new = st.text_input("New PIN", type="password")

        if st.button("Change"):
            if old == u["pin"]:
                u["pin"] = new
                save(data)
                st.success("PIN changed")
            else:
                st.error("Wrong PIN")