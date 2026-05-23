import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="FitMetrics Ultra Pro Max",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #050816,
        #0b1023,
        #111827,
        #1f2937
    );
    color: white;
}

/* Main Title */

.main-title {
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(to right,#00f5ff,#7c3aed,#ff00e5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* Subtitle */

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-bottom: 40px;
}

/* Glassmorphism Card */

.glass {
    background: rgba(255,255,255,0.08);
    border-radius: 25px;
    padding: 25px;
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.37);
}

/* Metric Cards */

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.08),
        rgba(255,255,255,0.03)
    );

    padding: 25px;
    border-radius: 25px;
    text-align: center;

    border: 1px solid rgba(255,255,255,0.1);

    box-shadow:
    0 0 15px rgba(0,255,255,0.2),
    0 0 30px rgba(124,58,237,0.2);

    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
}

.metric-title {
    color: #cbd5e1;
    font-size: 18px;
}

.metric-value {
    font-size: 42px;
    font-weight: 700;
    color: #00f5ff;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: rgba(17,24,39,0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Buttons */

.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 18px;
    border: none;
    font-size: 20px;
    font-weight: 700;
    color: white;
    background: linear-gradient(
        90deg,
        #06b6d4,
        #7c3aed,
        #ec4899
    );

    box-shadow:
    0 0 15px rgba(124,58,237,0.5);

    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
}

/* Slider */

.stSlider > div > div {
    color: cyan;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "gym_members_exercise_tracking.csv")

df = pd.read_csv(csv_path)

# ---------------- MODEL TRAINING ----------------

df_encoded = pd.get_dummies(df, drop_first=True)

target = "Calories_Burned"

X = df_encoded.drop(columns=[target])
y = df_encoded[target]

model_columns = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

accuracy = r2_score(y_test, model.predict(X_test))

# ---------------- HEADER ----------------

st.markdown(
    """
    <div class="main-title">
        🔥 FitMetrics Ultra Pro Max
    </div>

    <div class="subtitle">
        AI Powered 3D Fitness Intelligence Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## ⚡ User Controls")

age = st.sidebar.slider("🎂 Age", 15, 70, 25)

weight = st.sidebar.slider("⚖️ Weight (kg)", 40, 150, 70)

height = st.sidebar.slider("📏 Height (m)", 1.2, 2.2, 1.75)

max_bpm = st.sidebar.slider("❤️ Max BPM", 60, 220, 180)

avg_bpm = st.sidebar.slider("💓 Avg BPM", 50, 200, 120)

resting_bpm = st.sidebar.slider("🛌 Resting BPM", 40, 100, 70)

session_duration = st.sidebar.slider(
    "⏱️ Session Duration",
    0.5,
    5.0,
    1.5
)

fat_percentage = st.sidebar.slider(
    "🥩 Fat Percentage",
    5,
    50,
    20
)

water_intake = st.sidebar.slider(
    "💧 Water Intake",
    1.0,
    10.0,
    3.0
)

workout_frequency = st.sidebar.slider(
    "🏋️ Workout Frequency",
    1,
    14,
    5
)

experience_level = st.sidebar.slider(
    "🚀 Experience Level",
    1,
    5,
    3
)

bmi = weight / (height ** 2)

# ---------------- INPUT DATA ----------------

input_dict = {
    'Age': age,
    'Weight (kg)': weight,
    'Height (m)': height,
    'Max_BPM': max_bpm,
    'Avg_BPM': avg_bpm,
    'Resting_BPM': resting_bpm,
    'Session_Duration (hours)': session_duration,
    'Fat_Percentage': fat_percentage,
    'Water_Intake (liters)': water_intake,
    'Workout_Frequency (days/week)': workout_frequency,
    'Experience_Level': experience_level,
    'BMI': bmi
}

input_df = pd.DataFrame([input_dict])

input_df = pd.get_dummies(input_df)

for col in model_columns:
    if col not in input_df.columns:
        input_df[col] = 0

input_df = input_df[model_columns]

# ---------------- PREDICTION ----------------

if st.button("🚀 Predict Calories Burned"):

    prediction = model.predict(input_df)[0]

    st.balloons()

    st.markdown("## ⚡ AI Prediction Results")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔥 Calories Burned</div>
            <div class="metric-value">{prediction:.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📊 BMI</div>
            <div class="metric-value">{bmi:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎯 AI Accuracy</div>
            <div class="metric-value">{accuracy*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- BMI STATUS ----------------

    st.markdown("## 🧠 Health Analysis")

    if bmi < 18.5:
        st.warning("⚠️ Underweight Category")
    elif bmi < 25:
        st.success("✅ Healthy Category")
    elif bmi < 30:
        st.warning("⚠️ Overweight Category")
    else:
        st.error("🚨 Obesity Risk")

# ---------------- CHARTS ----------------

st.markdown("## 📈 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:

    fig1 = px.scatter(
        df,
        x="Age",
        y="Calories_Burned",
        size="Session_Duration (hours)",
        color="Experience_Level",
        title="Age vs Calories Burned"
    )

    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    fig2 = px.histogram(
        df,
        x="BMI",
        nbins=20,
        title="BMI Distribution"
    )

    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- DATASET ----------------

st.markdown("## 📂 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ---------------- FOOTER ----------------

st.markdown("""
<br><br>

<div style='text-align:center;color:gray;font-size:18px;'>

⚡ Designed with Streamlit + AI + Plotly <br>

🔥 Ultra Pro Max Dark 3D Edition

</div>
""", unsafe_allow_html=True)