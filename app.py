import streamlit as st

st.set_page_config(
    page_title="Employee Attrition AI",
    page_icon="🏢",
    layout="wide"
)

try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

st.title("🏢 Employee Attrition Prediction System")
st.markdown("""
## 🚀 AI Powered HR Analytics Dashboard

### Features

✅ Employee Attrition Prediction

✅ Analytics Dashboard

✅ Prediction History

✅ CSV Export

✅ 3D Interactive Charts

✅ Database Storage
""")

st.info(
    "Open the pages from the left sidebar."
)