import streamlit as st
from pathlib import Path
import shutil
from collections import Counter

st.set_page_config(page_title="File Manager Pro", page_icon="📂", layout="wide")

st.title("📂 File Manager Pro – Day 3 Project")
st.write("All file tools in one place 🚀")

# ---------------- PATH INPUT ----------------
base_path_input = st.text_input("Enter Folder Path", value=".")
base_path = Path(base_path_input)

if not base_path.exists():
    st.error("❌ Path does not exist")
    st.stop()


# =====================================================
# ✅ 1. COUNT FILES
# =====================================================
st.header("📊 File Statistics")

files = [f for f in base_path.rglob("*") if f.is_file()]

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Files", len(files))

with col2:
    exts = [f.suffix.lower() for f in files]
    counter = Counter(exts)
    st.write("### Extension Count")
    for k, v in counter.items():
        st.write(f"{k} : {v}")


# =====================================================
# ✅ 2. RENAME FILES
# =====================================================
st.header("✏️ Rename Files")

prefix = st.text_input("Enter prefix name (example: photo)")

if st.button("Rename All Files"):
    for i, f in enumerate(files, 1):
        new_name = f"{prefix}{i}{f.suffix}"
        f.rename(base_path / new_name)
    st.success("✅ Files renamed successfully!")


# =====================================================
# ✅ 3. DELETE FILE
# =====================================================
st.header("🗑 Delete File")

file_names = [f.name for f in files]

delete_file = st.selectbox("Select file to delete", file_names)

if st.button("Delete Selected File"):
    (base_path / delete_file).unlink()
    st.success("✅ File deleted!")


# =====================================================
# ✅ 4. MOVE FILE
# =====================================================
st.header("📦 Move File")

move_file = st.selectbox("Select file to move", file_names, key="move")

target_folder = st.text_input("Target folder name")

if st.button("Move File"):
    dest_folder = base_path / target_folder
    dest_folder.mkdir(exist_ok=True)
    shutil.move(str(base_path / move_file), dest_folder / move_file)
    st.success("✅ File moved!")


# =====================================================
# ✅ 5. AUTO ORGANIZER (Task D)
# =====================================================
st.header("🤖 Auto Organizer")

def organize_files():

    folders = {
        "images": [".jpg", ".png", ".jpeg", ".gif"],
        "documents": [".pdf", ".txt", ".docx"],
        "python_files": [".py"],
        "videos": [".mp4", ".mkv"],
        "others": []
    }

    moved = []
    count = 0

    for folder in folders:
        (base_path / folder).mkdir(exist_ok=True)

    for file in base_path.iterdir():

        if file.is_file():

            placed = False

            for folder, exts in folders.items():
                if file.suffix.lower() in exts:
                    shutil.move(str(file), base_path / folder / file.name)
                    moved.append(f"{file.name} → {folder}")
                    count += 1
                    placed = True
                    break

            if not placed:
                shutil.move(str(file), base_path / "others" / file.name)
                moved.append(f"{file.name} → others")
                count += 1

    st.success(f"✅ {count} files organized!")

    for m in moved:
        st.write(m)


if st.button("🚀 Run Auto Organizer"):
    organize_files()