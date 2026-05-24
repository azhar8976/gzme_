import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="🎬 Movie Prediction AI",
    page_icon="🎬",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg,#030712,#0f172a,#111827);
    color: white;
}

/* MAIN APP */
.main {
    background: transparent;
}

/* TOP SPACE */
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* HEADINGS */
h1,h2,h3,h4 {
    color: #00F5FF;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0,255,255,0.15);
}

/* DATAFRAME */
div[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* BUTTON */
.stButton button {
    background: linear-gradient(45deg,#00F5FF,#7C3AED);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    padding: 12px 22px;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(0,255,255,0.5);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* CHART BOX */
.chart-box {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* SUCCESS BOX */
.stSuccess {
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="text-align:center;padding:20px;">

<h1 style="font-size:55px;">
🎬 MOVIE PREDICTION AI DASHBOARD
</h1>

<h3 style="color:#94A3B8;">
⚡ Ultra Interactive Machine Learning Experience ⚡
</h3>

</div>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "mymoviedb.csv",
        engine="python",
        on_bad_lines='skip',
        encoding='latin1'
    )

    return df

# =====================================================
# PREPROCESS
# =====================================================

@st.cache_data
def preprocess(df):

    df = df.copy()

    # DATE

    df['Release_Date'] = pd.to_datetime(
        df['Release_Date'],
        errors='coerce'
    )

    df['Release_Year'] = df['Release_Date'].dt.year

    # DROP COLUMNS

    drop_cols = [
        'Overview',
        'Original_Language',
        'Poster_Url',
        'Release_Date'
    ]

    for col in drop_cols:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

    # GENRE

    df['Genre'] = df['Genre'].fillna("Unknown")

    df['Genre'] = df['Genre'].apply(
        lambda x: str(x).split(',')[0]
    )

    # CLEAN Vote_Count

    df['Vote_Count'] = (
        df['Vote_Count']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.strip()
    )

    df['Vote_Count'] = pd.to_numeric(
        df['Vote_Count'],
        errors='coerce'
    )

    # CLEAN Vote_Average

    df['Vote_Average'] = pd.to_numeric(
        df['Vote_Average'],
        errors='coerce'
    )

    # REMOVE NULLS

    df.dropna(
        subset=['Vote_Count', 'Vote_Average'],
        inplace=True
    )

    # CATEGORY SYSTEM

    df['Vote_Category'] = np.where(
        df['Vote_Count'] < 1000,
        'Low',

        np.where(
            df['Vote_Count'] < 5000,
            'Medium',

            np.where(
                df['Vote_Count'] < 10000,
                'High',
                'Very High'
            )
        )
    )

    # ENCODING

    df = pd.get_dummies(
        df,
        columns=['Genre', 'Vote_Category'],
        drop_first=True
    )

    # REMOVE TITLE

    if 'Title' in df.columns:
        df.drop('Title', axis=1, inplace=True)

    # FINAL CLEAN

    df.dropna(inplace=True)

    return df

# =====================================================
# EVALUATE
# =====================================================

def evaluate(y_true, y_pred):

    mae = mean_absolute_error(y_true, y_pred)

    mse = mean_squared_error(y_true, y_pred)

    rmse = np.sqrt(mse)

    r2 = r2_score(y_true, y_pred)

    return mae, mse, rmse, r2

# =====================================================
# TRAIN MODELS
# =====================================================

@st.cache_resource
def train_models(df):

    X = df.drop('Vote_Average', axis=1)

    y = df['Vote_Average']

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {

        "Random Forest":
        RandomForestRegressor(
            n_estimators=150,
            random_state=42
        ),

        "Linear Regression":
        LinearRegression(),

        "Gradient Boosting":
        GradientBoostingRegressor(
            random_state=42
        )
    }

    results = {}

    progress = st.progress(0)

    for i, (name, model) in enumerate(models.items()):

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        mae, mse, rmse, r2 = evaluate(
            y_test,
            preds
        )

        results[name] = {

            "model": model,

            "preds": preds,

            "metrics": {

                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse,
                "R2": r2
            }
        }

        progress.progress((i + 1) / len(models))

    return results, X_test, y_test

# =====================================================
# MAIN
# =====================================================

with st.spinner("🚀 Loading AI Engine..."):

    raw_df = load_data()

    processed_df = preprocess(raw_df)

with st.spinner("🤖 Training Models..."):

    results, X_test, y_test = train_models(processed_df)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Dashboard Controls")

selected_model = st.sidebar.selectbox(
    "🎯 Select Model",
    list(results.keys())
)

show_data = st.sidebar.checkbox("📂 Show Dataset")

show_corr = st.sidebar.checkbox("🔥 Show Heatmap")

# =====================================================
# METRICS
# =====================================================

metrics_df = pd.DataFrame({

    model: results[model]['metrics']
    for model in results

}).T

best_model = metrics_df['R2'].idxmax()

best_r2 = metrics_df['R2'].max()

lowest_rmse = metrics_df['RMSE'].min()

# =====================================================
# METRIC CARDS
# =====================================================

st.markdown("## 📊 AI Model Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏆 Best Model", best_model)

c2.metric("📈 Best R²", round(best_r2, 4))

c3.metric("📉 Lowest RMSE", round(lowest_rmse, 4))

c4.metric("🧠 Total Models", len(results))

# =====================================================
# METRICS TABLE
# =====================================================

st.markdown("## 📋 Model Metrics Table")

st.dataframe(
    metrics_df,
    width='stretch'
)

# =====================================================
# 3D VISUALIZATION
# =====================================================

st.markdown("## 🚀 3D Model Performance")

fig_3d = go.Figure()

for model in metrics_df.index:

    fig_3d.add_trace(

        go.Scatter3d(

            x=[metrics_df.loc[model, 'MAE']],
            y=[metrics_df.loc[model, 'RMSE']],
            z=[metrics_df.loc[model, 'R2']],

            mode='markers+text',

            text=[model],

            marker=dict(
                size=12
            )
        )
    )

fig_3d.update_layout(

    template="plotly_dark",

    paper_bgcolor='rgba(0,0,0,0)',

    plot_bgcolor='rgba(0,0,0,0)',

    height=700,

    scene=dict(

        xaxis_title='MAE',
        yaxis_title='RMSE',
        zaxis_title='R2 Score'
    )
)

st.plotly_chart(
    fig_3d,
    width='stretch'
)

# =====================================================
# PREDICTION ANALYSIS
# =====================================================

st.markdown(f"## 🎯 {selected_model} Prediction Analysis")

preds = results[selected_model]['preds']

prediction_df = pd.DataFrame({

    "Actual": y_test,
    "Predicted": preds

})

# REMOVED trendline="ols"
# because statsmodels error aa raha tha

fig_pred = px.scatter(

    prediction_df,

    x="Actual",

    y="Predicted",

    title=f"{selected_model} Predictions",

    opacity=0.7
)

fig_pred.update_layout(

    template="plotly_dark",

    paper_bgcolor='rgba(0,0,0,0)',

    plot_bgcolor='rgba(0,0,0,0)',

    height=600
)

st.plotly_chart(
    fig_pred,
    width='stretch'
)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

if selected_model == "Random Forest":

    st.markdown("## 🔥 Top Feature Importance")

    rf_model = results[selected_model]['model']

    importance_df = pd.DataFrame({

        "Feature": X_test.columns,

        "Importance": rf_model.feature_importances_

    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    ).head(15)

    fig_bar = px.bar(

        importance_df,

        x="Importance",

        y="Feature",

        orientation='h'
    )

    fig_bar.update_layout(

        template="plotly_dark",

        paper_bgcolor='rgba(0,0,0,0)',

        plot_bgcolor='rgba(0,0,0,0)',

        height=650
    )

    st.plotly_chart(
        fig_bar,
        width='stretch'
    )

# =====================================================
# HEATMAP
# =====================================================

if show_corr:

    st.markdown("## 🔥 Correlation Heatmap")

    corr = processed_df.corr(numeric_only=True)

    fig_heat = px.imshow(
        corr,
        aspect="auto"
    )

    fig_heat.update_layout(

        template="plotly_dark",

        paper_bgcolor='rgba(0,0,0,0)',

        plot_bgcolor='rgba(0,0,0,0)',

        height=900
    )

    st.plotly_chart(
        fig_heat,
        width='stretch'
    )

# =====================================================
# DATASET
# =====================================================

if show_data:

    st.markdown("## 📂 Dataset Preview")

    st.dataframe(
        raw_df.head(100),
        width='stretch'
    )

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

csv = metrics_df.to_csv().encode('utf-8')

st.download_button(

    "📥 Download Metrics CSV",

    csv,

    "movie_metrics.csv",

    "text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.success("✅ Ultra AI Dashboard Running Successfully")

st.markdown("""

## 🌟 Features Included

- ✅ 3D Visualization
- ✅ Interactive Graphs
- ✅ Machine Learning Models
- ✅ Prediction Analysis
- ✅ Feature Importance
- ✅ Correlation Heatmap
- ✅ Download Reports
- ✅ Modern Dark UI

""")