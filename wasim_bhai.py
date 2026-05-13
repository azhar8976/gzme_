# import streamlit as st
# import sqlite3
# from datetime import datetime
# import matplotlib.pyplot as plt
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from openpyxl import Workbook
# import urllib.parse

# # ================= PAGE CONFIG =================
# st.set_page_config(
#     page_title="Wasim Bhai Orders",
#     page_icon="😋",
#     layout="wide"
# )

# # ================= STYLE =================
# st.markdown("""
# <style>
# .block-container {padding-top: 1rem;}
# .stButton>button {
#     border-radius:12px;
#     height:40px;
#     font-weight:bold;
# }
# </style>
# """, unsafe_allow_html=True)


# # =================================================
# # ================= DATABASE (FIXED) ===============
# # =================================================
# conn = sqlite3.connect("orders.db", check_same_thread=False)
# c = conn.cursor()

# # 🔥 AUTO FIX (important)
# # old wrong structure delete → new correct create
# c.execute("DROP TABLE IF EXISTS orders")

# c.execute("""
# CREATE TABLE orders(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     item TEXT,
#     price INTEGER,
#     status TEXT,
#     time TEXT
# )
# """)

# c.execute("""
# CREATE TABLE IF NOT EXISTS users(
#     username TEXT,
#     password TEXT,
#     role TEXT
# )
# """)

# conn.commit()


# # default admin
# c.execute("SELECT * FROM users WHERE username='admin'")
# if not c.fetchone():
#     c.execute("INSERT INTO users VALUES('admin','1234','admin')")
#     conn.commit()


# # ================= SESSION =================
# if "login" not in st.session_state:
#     st.session_state.login = False
# if "role" not in st.session_state:
#     st.session_state.role = ""


# # ======================================================
# # ================= LOGIN / SIGNUP =====================
# # ======================================================
# if not st.session_state.login:

#     st.title("😋 Wasim Bhai Orders")

#     tab1, tab2 = st.tabs(["Login", "Signup"])

#     # LOGIN
#     with tab1:
#         u = st.text_input("Username")
#         p = st.text_input("Password", type="password")

#         if st.button("Login"):
#             user = c.execute(
#                 "SELECT role FROM users WHERE username=? AND password=?",
#                 (u, p)
#             ).fetchone()

#             if user:
#                 st.session_state.login = True
#                 st.session_state.role = user[0]
#                 st.rerun()
#             else:
#                 st.error("Wrong login")

#     # SIGNUP
#     with tab2:
#         nu = st.text_input("New username")
#         np = st.text_input("New password", type="password")

#         if st.button("Create Account"):
#             c.execute("INSERT INTO users VALUES(?,?,'customer')", (nu, np))
#             conn.commit()
#             st.success("Account created! Login now")

#     st.stop()


# # ======================================================
# # ====================== ADMIN =========================
# # ======================================================
# if st.session_state.role == "admin":

#     st.header("🛠 Admin Dashboard")

#     rows = c.execute("SELECT * FROM orders").fetchall()

#     if not rows:
#         st.info("No orders yet")

#     total = sum(r[3] for r in rows)
#     st.metric("💰 Total Sales", f"₹ {total}")

#     search = st.text_input("🔍 Search")

#     if search:
#         rows = [r for r in rows if search.lower() in str(r).lower()]

#     for r in rows:

#         col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,1,1,1,1,1])

#         col1.write(r[1])
#         col2.write(r[2])
#         col3.write(r[3])

#         status = col4.selectbox(
#             "",
#             ["Pending", "Delivered"],
#             index=0 if r[4] == "Pending" else 1,
#             key=f"s{r[0]}"
#         )

#         c.execute("UPDATE orders SET status=? WHERE id=?", (status, r[0]))
#         conn.commit()

#         if col5.button("❌", key=f"d{r[0]}"):
#             c.execute("DELETE FROM orders WHERE id=?", (r[0],))
#             conn.commit()
#             st.rerun()

#         msg = f"{r[1]} ordered {r[2]} ₹{r[3]}"
#         url = "https://wa.me/?text=" + urllib.parse.quote(msg)
#         col6.markdown(f"[📤]({url})")

#         # PDF
#         if col7.button("🧾", key=f"pdf{r[0]}"):
#             file = f"bill_{r[0]}.pdf"
#             doc = SimpleDocTemplate(file)
#             styles = getSampleStyleSheet()

#             elements = [
#                 Paragraph("Order Bill", styles["Heading1"]),
#                 Spacer(1, 20),
#                 Paragraph(f"Name: {r[1]}", styles["BodyText"]),
#                 Paragraph(f"Item: {r[2]}", styles["BodyText"]),
#                 Paragraph(f"Price: ₹{r[3]}", styles["BodyText"]),
#                 Paragraph(f"Status: {r[4]}", styles["BodyText"]),
#             ]

#             doc.build(elements)

#             with open(file, "rb") as f:
#                 st.download_button("Download Bill", f, file_name=file)

#     # Excel
#     if st.button("📥 Download Excel"):
#         wb = Workbook()
#         ws = wb.active
#         ws.append(["ID", "Name", "Item", "Price", "Status", "Time"])

#         for r in rows:
#             ws.append(r)

#         file = "orders.xlsx"
#         wb.save(file)

#         with open(file, "rb") as f:
#             st.download_button("Download Excel File", f, file_name=file)

#     # Charts
#     prices = [r[3] for r in rows]

#     fig = plt.figure()
#     plt.bar(range(len(prices)), prices)
#     st.pyplot(fig)

#     fig2 = plt.figure()
#     plt.pie(prices)
#     st.pyplot(fig2)

#     if st.button("Logout"):
#         st.session_state.login = False
#         st.rerun()


# # ======================================================
# # ================= CUSTOMER ===========================
# # ======================================================
# else:

#     st.header("🛒 Place Order")

#     name = st.text_input("Name")
#     item = st.text_input("Item")
#     price = st.number_input("Price", min_value=0)

#     if st.button("Place Order 🚀"):
#         c.execute(
#             "INSERT INTO orders(name,item,price,status,time) VALUES (?,?,?,?,?)",
#             (name, item, price, "Pending", str(datetime.now()))
#         )
#         conn.commit()

#         st.success("Order placed successfully")

#     if st.button("Logout"):
#         st.session_state.login = False
#         st.rerun()



