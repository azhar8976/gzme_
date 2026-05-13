import streamlit as st
import sqlite3
import hashlib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Member App", page_icon="📱", layout="centered")

# ---------------- DARK THEME ----------------
st.markdown("""
<style>
body {background-color:#0e1117; color:white;}
.stTextInput>div>div>input {background:#262730;color:white;}
.stTextArea textarea {background:#262730;color:white;}
</style>
""", unsafe_allow_html=True)

st.title("📱 Member App")
st.caption("Instagram Style • Made by Azzu ❤️")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("member.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
photo BLOB)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS posts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
text TEXT,
likes INTEGER DEFAULT 0)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS comments(
post_id INTEGER,
user TEXT,
comment TEXT)
""")

conn.commit()


# ---------------- PASSWORD HASH ----------------
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None


# ==================================================
# 🔐 LOGIN / REGISTER
# ==================================================
if not st.session_state.user:

    st.subheader("🔐 Login / Register")

    choice = st.radio("Choose", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    photo = st.file_uploader("Profile Photo (register only)", type=["png","jpg","jpeg"])

    # -------- REGISTER --------
    if choice == "Register":
        if st.button("Create Account"):
            if username and password:
                img = photo.read() if photo else None
                c.execute(
                    "INSERT INTO users VALUES(?,?,?)",
                    (username, hash_pass(password), img)
                )
                conn.commit()
                st.success("Account created ✅ Now Login")

    # -------- LOGIN --------
    if choice == "Login":
        if st.button("Login"):
            user = c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, hash_pass(password))
            ).fetchone()

            if user:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Wrong username or password ❌")


# ==================================================
# AFTER LOGIN
# ==================================================
if st.session_state.user:

    user = st.session_state.user

    st.divider()
    st.subheader(f"👤 Welcome {user}")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

    # -------- PROFILE PHOTO --------
    photo = c.execute("SELECT photo FROM users WHERE username=?", (user,)).fetchone()
    if photo and photo[0]:
        st.image(photo[0], width=120)

    # -------- CREATE POST --------
    st.divider()
    st.subheader("➕ Create Post")

    text = st.text_area("Write something...")

    if st.button("Post"):
        if text:
            c.execute("INSERT INTO posts(user,text,likes) VALUES(?,?,0)", (user, text))
            conn.commit()
            st.rerun()

    # -------- FEED --------
    st.divider()
    st.subheader("📰 Feed")

    posts = c.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()

    for post_id, p_user, p_text, likes in posts:

        st.markdown(f"### 👤 {p_user}")
        st.write(p_text)

        col1, col2 = st.columns(2)

        # ❤️ LIKE
        with col1:
            if st.button(f"❤️ Like ({likes})", key=f"like{post_id}"):
                c.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
                conn.commit()
                st.rerun()

        # 💬 COMMENT
        with col2:
            comment = st.text_input("Comment", key=f"c{post_id}")
            if st.button("Send", key=f"s{post_id}"):
                if comment:
                    c.execute("INSERT INTO comments VALUES(?,?,?)", (post_id, user, comment))
                    conn.commit()
                    st.rerun()

        comments = c.execute("SELECT user,comment FROM comments WHERE post_id=?", (post_id,)).fetchall()

        for u, com in comments:
            st.write(f"💬 {u}: {com}")

        st.divider()


# ---------------- FOOTER ----------------
st.markdown("""
<center>
❤️ Made by Azzu <br>
🚀 Member App Pro Version
</center>
""", unsafe_allow_html=True)
