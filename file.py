import streamlit as st
from pathlib import Path
import shutil

st.set_page_config(page_title="File Manager", page_icon="📁", layout="centered")

st.title("📁 Simple File Manager")

BASE_PATH = Path(".")


# ---------------- CREATE FOLDER ----------------
def create_folder(name):
    p = BASE_PATH / name
    if not p.exists():
        p.mkdir()
        st.success("✅ Folder created successfully")
    else:
        st.warning("⚠️ Folder already exists")


# ---------------- LIST FILES ----------------
def list_files():
    items = list(BASE_PATH.rglob("*"))
    return [str(i) for i in items]


# ---------------- DELETE ----------------
def delete_path(name):
    p = Path(name)

    if p.exists():
        if p.is_file():
            p.unlink()
        else:
            shutil.rmtree(p)

        st.success("🗑 Deleted successfully")
    else:
        st.error("❌ Path not found")


# ================= UI =================

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Create Folder", "List Files", "Delete File/Folder"]
)


# ---- CREATE ----
if menu == "Create Folder":
    st.subheader("Create Folder")

    folder_name = st.text_input("Enter folder name")

    if st.button("Create"):
        if folder_name:
            create_folder(folder_name)


# ---- LIST ----
elif menu == "List Files":
    st.subheader("All Files & Folders")

    files = list_files()

    if files:
        st.write(files)
    else:
        st.info("Empty directory")


# ---- DELETE ----
elif menu == "Delete File/Folder":
    st.subheader("Delete File/Folder")

    files = list_files()

    selected = st.selectbox("Select file/folder", files)

    if st.button("Delete"):
        delete_path(selected)
