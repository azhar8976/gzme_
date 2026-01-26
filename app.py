import streamlit as st
from pathlib import Path
import os
import shutil
import pandas as pd
import zipfile
import time

st.set_page_config(page_title="Azzu Ultimate File Explorer", layout="wide")

BASE_PATH = Path.cwd()

st.title("🚀 Azzu Ultimate File Explorer")
st.caption("Advanced Streamlit File Manager with Drag & Drop, Zip, Multi Select, Preview")


# =====================================================
# Helpers
# =====================================================

def icon(path: Path):
    return "📁" if path.is_dir() else "📄"


def file_dataframe():
    rows = []

    for p in BASE_PATH.rglob("*"):
        rows.append({
            "Icon": icon(p),
            "Name": p.name,
            "Type": "Folder" if p.is_dir() else "File",
            "Size (KB)": round(p.stat().st_size / 1024, 2),
            "Path": str(p)
        })

    return pd.DataFrame(rows)


def make_zip(files, zip_name="files.zip"):
    with zipfile.ZipFile(zip_name, "w") as z:
        for f in files:
            z.write(f, arcname=Path(f).name)
    return zip_name


# =====================================================
# Sidebar Menu
# =====================================================

menu = st.sidebar.radio(
    "📌 Menu",
    [
        "Dashboard",
        "Upload (Drag & Drop)",
        "Create",
        "Preview / Download",
        "Rename",
        "Delete",
        "Zip Download"
    ]
)


# =====================================================
# 1️⃣ Dashboard
# =====================================================

if menu == "Dashboard":

    st.subheader("📊 File Explorer Dashboard")

    df = file_dataframe()

    search = st.text_input("🔍 Search")

    filter_type = st.selectbox("Filter", ["All", "File", "Folder"])

    if search:
        df = df[df["Name"].str.contains(search, case=False)]

    if filter_type != "All":
        df = df[df["Type"] == filter_type]

    st.dataframe(df, use_container_width=True)


# =====================================================
# 2️⃣ Drag & Drop Upload + Progress bar
# =====================================================

elif menu == "Upload (Drag & Drop)":

    st.subheader("⬆ Drag & Drop Upload")

    files = st.file_uploader(
        "Drop files here",
        accept_multiple_files=True
    )

    if files:
        progress = st.progress(0)

        for i, file in enumerate(files):

            with open(file.name, "wb") as f:
                f.write(file.getbuffer())

            time.sleep(0.2)
            progress.progress((i + 1) / len(files))

        st.success("All files uploaded ✅")


# =====================================================
# 3️⃣ Create
# =====================================================

elif menu == "Create":

    tab1, tab2 = st.tabs(["📁 Folder", "📄 File"])

    with tab1:
        name = st.text_input("Folder name")

        if st.button("Create Folder"):
            (BASE_PATH / name).mkdir(exist_ok=True)
            st.success("Folder created")

    with tab2:
        name = st.text_input("File name")
        content = st.text_area("Content")

        if st.button("Create File"):
            with open(name, "w") as f:
                f.write(content)
            st.success("File created")


# =====================================================
# 4️⃣ Preview + Download
# =====================================================

elif menu == "Preview / Download":

    st.subheader("📖 Preview & Download")

    name = st.text_input("File name")

    if st.button("Open"):

        p = BASE_PATH / name

        if p.exists() and p.is_file():

            with open(p, "r", errors="ignore") as f:
                st.text_area("Content", f.read(), height=300)

            with open(p, "rb") as f:
                st.download_button("⬇ Download", f, file_name=name)

        else:
            st.error("File not found")


# =====================================================
# 5️⃣ Rename
# =====================================================

elif menu == "Rename":

    st.subheader("✏ Rename")

    old = st.text_input("Old name")
    new = st.text_input("New name")

    if st.button("Rename"):
        old_p = BASE_PATH / old
        new_p = BASE_PATH / new

        if old_p.exists():
            old_p.rename(new_p)
            st.success("Renamed successfully")
        else:
            st.error("Not found")


# =====================================================
# 6️⃣ Delete (Multi select)
# =====================================================

elif menu == "Delete":

    st.subheader("🗑 Delete Multiple")

    df = file_dataframe()

    selected = st.multiselect("Select files/folders", df["Path"])

    confirm = st.checkbox("Confirm delete")

    if st.button("Delete Selected") and confirm:

        for item in selected:
            p = Path(item)

            if p.is_dir():
                shutil.rmtree(p)
            else:
                os.remove(p)

        st.success("Deleted successfully")


# =====================================================
# 7️⃣ Zip Download (Multiple select)
# =====================================================

elif menu == "Zip Download":

    st.subheader("📦 Zip Multiple Files")

    df = file_dataframe()

    selected = st.multiselect("Select files", df[df["Type"] == "File"]["Path"])

    if st.button("Create Zip") and selected:

        zip_name = make_zip(selected)

        with open(zip_name, "rb") as f:
            st.download_button("⬇ Download ZIP", f, file_name="files.zip")

        os.remove(zip_name)

