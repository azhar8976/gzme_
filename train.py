"""
╔══════════════════════════════════════════════════════════╗
║   ATTRITION INTELLIGENCE PLATFORM  —  Ultra Pro Max      ║
║   XGBoost · Plotly · Streamlit · Real-time Predictions   ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import io
import time
import os
warnings.filterwarnings("ignore")

# ── Resolve file paths relative to this script ──
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "xgboost_model.pkl")
CSV_PATH   = os.path.join(BASE_DIR, "test.csv")

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    roc_auc_score, roc_curve, precision_recall_curve
)

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AttritionIQ — Employee Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  — DARK LUXURY THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

:root {
    --bg-primary:    #0a0a0f;
    --bg-card:       #12121a;
    --bg-card2:      #1a1a26;
    --accent:        #7c6af7;
    --accent2:       #f97316;
    --accent3:       #10b981;
    --danger:        #ef4444;
    --text-primary:  #f0f0f8;
    --text-muted:    #8888a8;
    --border:        rgba(124,106,247,0.18);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0e1a 0%, #12121e 100%) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.85rem; }

/* ── Main area ── */
[data-testid="stMain"], .main { background: var(--bg-primary) !important; }
.block-container { padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1600px; }

/* ── Headers ── */
h1 { font-family: 'DM Serif Display', serif !important; font-size: 2.4rem !important;
     background: linear-gradient(135deg, #a78bfa, #7c6af7, #f97316);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
h2, h3 { font-family: 'DM Serif Display', serif !important; color: var(--text-primary) !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
    transition: transform .2s, box-shadow .2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(124,106,247,0.18);
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.75rem !important; letter-spacing: .06em; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: var(--text-primary) !important; font-size: 1.9rem !important; font-weight: 700; }
[data-testid="stMetricDelta"] svg { display:none; }

/* ── Selectbox / input ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] > div,
[data-testid="stSlider"] { background: var(--bg-card2) !important; border-radius: 10px !important; }

/* ── Tabs ── */
[data-testid="stTabs"] button {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 500; padding: .6rem 1.2rem;
    transition: color .2s, border-color .2s;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5b46e0) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: .55rem 1.6rem !important;
    font-weight: 600 !important; font-size: .9rem !important;
    letter-spacing: .02em;
    transition: opacity .2s, transform .2s !important;
    box-shadow: 0 4px 20px rgba(124,106,247,0.35);
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden; }
[data-testid="stDataFrame"] * { font-size: .82rem !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ── Plotly chart background ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Risk badge cards ── */
.risk-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: .8rem;
    transition: transform .2s;
}
.risk-card:hover { transform: translateX(4px); }

/* ── Alert boxes ── */
.alert-high   { border-left: 4px solid var(--danger)  !important; background: rgba(239,68,68,.08)  !important; }
.alert-medium { border-left: 4px solid var(--accent2) !important; background: rgba(249,115,22,.08) !important; }
.alert-low    { border-left: 4px solid var(--accent3) !important; background: rgba(16,185,129,.08) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 3px; }

/* ── Section separator ── */
.sep { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── Subtitle ── */
.subtitle { color: var(--text-muted); font-size: .95rem; margin-top: -.8rem; margin-bottom: 1.8rem; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
FEATURES = [
    'Age', 'Gender', 'Years at Company', 'Job Role', 'Monthly Income',
    'Work-Life Balance', 'Job Satisfaction', 'Performance Rating',
    'Number of Promotions', 'Overtime', 'Distance from Home',
    'Education Level', 'Marital Status', 'Number of Dependents',
    'Job Level', 'Company Size', 'Company Tenure', 'Remote Work',
    'Leadership Opportunities', 'Innovation Opportunities',
    'Company Reputation', 'Employee Recognition'
]
CAT_COLS = [
    'Gender', 'Job Role', 'Work-Life Balance', 'Job Satisfaction',
    'Performance Rating', 'Overtime', 'Education Level', 'Marital Status',
    'Job Level', 'Company Size', 'Remote Work', 'Leadership Opportunities',
    'Innovation Opportunities', 'Company Reputation', 'Employee Recognition'
]
NUM_COLS = [f for f in FEATURES if f not in CAT_COLS]

CAT_OPTIONS = {
    'Gender':                  ['Male', 'Female'],
    'Job Role':                ['Finance', 'Healthcare', 'Technology', 'Media', 'Education'],
    'Work-Life Balance':       ['Excellent', 'Good', 'Fair', 'Poor'],
    'Job Satisfaction':        ['Very High', 'High', 'Medium', 'Low'],
    'Performance Rating':      ['High', 'Average', 'Below Average', 'Low'],
    'Overtime':                ['No', 'Yes'],
    'Education Level':         ["Bachelor's Degree", "Master's Degree", 'Associate Degree', 'PhD', 'High School'],
    'Marital Status':          ['Married', 'Single', 'Divorced'],
    'Job Level':               ['Senior', 'Mid', 'Entry'],
    'Company Size':            ['Large', 'Medium', 'Small'],
    'Remote Work':             ['Yes', 'No'],
    'Leadership Opportunities':['Yes', 'No'],
    'Innovation Opportunities':['Yes', 'No'],
    'Company Reputation':      ['Excellent', 'Good', 'Fair', 'Poor'],
    'Employee Recognition':    ['Very High', 'High', 'Medium', 'Low'],
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(18,18,26,0.6)',
    font=dict(family='Inter', color='#f0f0f8'),
    margin=dict(t=40, b=30, l=40, r=20),
    colorway=['#7c6af7', '#f97316', '#10b981', '#f43f5e', '#38bdf8', '#facc15'],
)


# ─────────────────────────────────────────────
#  DATA / MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv(CSV_PATH)
    return df

@st.cache_data(show_spinner=False)
def preprocess(df: pd.DataFrame):
    X = df[FEATURES].copy()
    le = LabelEncoder()
    for col in CAT_COLS:
        X[col] = le.fit_transform(X[col].astype(str))
    return X

def predict_single(model, row_dict: dict):
    df = pd.DataFrame([row_dict])[FEATURES]
    le = LabelEncoder()
    for col in CAT_COLS:
        le.fit(CAT_OPTIONS[col])
        df[col] = le.transform(df[col].astype(str))
    prob = model.predict_proba(df)[0]
    return prob[1], prob[0]   # p_left, p_stayed


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 .5rem;'>
      <div style='font-size:2.5rem;'>🧬</div>
      <div style='font-size:1.15rem; font-weight:700; color:#a78bfa; letter-spacing:.04em;'>AttritionIQ</div>
      <div style='font-size:.72rem; color:#8888a8; margin-top:3px; letter-spacing:.08em;'>EMPLOYEE INTELLIGENCE PLATFORM</div>
    </div>
    <hr style='border:none; border-top:1px solid rgba(124,106,247,.2); margin:.8rem 0 1rem;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Dashboard", "🔮  Single Prediction", "📦  Batch Analysis",
         "📊  Model Insights", "🎯  Risk Profiler", "📋  Data Explorer"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border:none;border-top:1px solid rgba(124,106,247,.2);margin:1rem 0;'>", unsafe_allow_html=True)

    # Sidebar model info
    with st.expander("⚙️ Model Info", expanded=False):
        st.markdown("""
        <div style='font-size:.8rem; color:#8888a8;'>
        <b style='color:#a78bfa;'>Algorithm</b><br>XGBoost Classifier<br><br>
        <b style='color:#a78bfa;'>Features</b><br>22 employee attributes<br><br>
        <b style='color:#a78bfa;'>Classes</b><br>Left · Stayed<br><br>
        <b style='color:#a78bfa;'>Dataset</b><br>14,900 employees
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:.68rem;color:#555;text-align:center;margin-top:2rem;'>© 2025 AttritionIQ Platform</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOAD RESOURCES
# ─────────────────────────────────────────────
with st.spinner("Loading intelligence engine..."):
    model = load_model()
    df_raw = load_data()
    X_all  = preprocess(df_raw)

y_true = (df_raw['Attrition'] == 'Left').astype(int)
y_pred = model.predict(X_all)
y_prob = model.predict_proba(X_all)[:, 1]

acc    = accuracy_score(y_true, y_pred)
auc    = roc_auc_score(y_true, y_prob)
left   = (df_raw['Attrition'] == 'Left').sum()
stayed = (df_raw['Attrition'] == 'Stayed').sum()
high_risk_pct = (y_prob > 0.7).mean() * 100


# ══════════════════════════════════════════════════════════════
#  PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "🏠  Dashboard":
    st.markdown("# AttritionIQ Intelligence Platform")
    st.markdown("<p class='subtitle'>Real-time employee attrition analytics & prediction powered by XGBoost</p>", unsafe_allow_html=True)

    # ── KPI Row ──
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Employees", f"{len(df_raw):,}")
    c2.metric("Left Company",    f"{left:,}",   f"{left/len(df_raw)*100:.1f}%")
    c3.metric("Retained",        f"{stayed:,}", f"{stayed/len(df_raw)*100:.1f}%")
    c4.metric("Model AUC-ROC",   f"{auc:.3f}")
    c5.metric("High-Risk Pool",  f"{high_risk_pct:.1f}%")

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    # ── Attrition donut ──
    with col_l:
        st.markdown("### Attrition Breakdown")
        fig_pie = go.Figure(go.Pie(
            labels=['Stayed', 'Left'],
            values=[stayed, left],
            hole=.62,
            marker_colors=['#10b981', '#ef4444'],
            textinfo='label+percent',
            textfont=dict(size=13, family='Inter'),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>"
        ))
        fig_pie.add_annotation(text=f"<b>{len(df_raw):,}</b><br><span style='font-size:11px'>Employees</span>",
                               x=.5, y=.5, showarrow=False,
                               font=dict(size=16, color='#f0f0f8', family='Inter'))
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=True,
                              legend=dict(orientation='h', yanchor='bottom', y=-0.15))
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Attrition by Job Role ──
    with col_r:
        st.markdown("### Attrition Rate by Job Role")
        role_stats = df_raw.groupby('Job Role')['Attrition'].apply(
            lambda x: (x == 'Left').mean() * 100).reset_index()
        role_stats.columns = ['Job Role', 'Attrition Rate (%)']
        role_stats = role_stats.sort_values('Attrition Rate (%)', ascending=True)

        fig_bar = go.Figure(go.Bar(
            x=role_stats['Attrition Rate (%)'],
            y=role_stats['Job Role'],
            orientation='h',
            marker=dict(
                color=role_stats['Attrition Rate (%)'],
                colorscale=[[0,'#10b981'],[0.5,'#f97316'],[1,'#ef4444']],
                showscale=False
            ),
            text=[f"{v:.1f}%" for v in role_stats['Attrition Rate (%)']],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Attrition Rate: %{x:.1f}%<extra></extra>"
        ))
        fig_bar.update_layout(**PLOTLY_LAYOUT, height=300,
                              xaxis=dict(showgrid=False, visible=False),
                              yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar, use_container_width=True)

    col_l2, col_r2 = st.columns([1, 1])

    # ── Income vs Attrition violin ──
    with col_l2:
        st.markdown("### Monthly Income Distribution")
        fig_vio = go.Figure()
        fill_colors = {'Stayed': 'rgba(16,185,129,0.15)', 'Left': 'rgba(239,68,68,0.15)'}
        for label, color in [('Stayed', '#10b981'), ('Left', '#ef4444')]:
            vals = df_raw[df_raw['Attrition'] == label]['Monthly Income']
            fig_vio.add_trace(go.Violin(y=vals, name=label, line_color=color,
                                        fillcolor=fill_colors[label],
                                        box_visible=True, meanline_visible=True,
                                        points=False))
        fig_vio.update_layout(**PLOTLY_LAYOUT, height=310, yaxis_title="Monthly Income ($)")
        st.plotly_chart(fig_vio, use_container_width=True)

    # ── Age histogram ──
    with col_r2:
        st.markdown("### Age Distribution by Attrition")
        fig_hist = go.Figure()
        for label, color in [('Stayed', '#7c6af7'), ('Left', '#f97316')]:
            vals = df_raw[df_raw['Attrition'] == label]['Age']
            fig_hist.add_trace(go.Histogram(x=vals, name=label, nbinsx=25,
                                            marker_color=color, opacity=0.72))
        fig_hist.update_layout(**PLOTLY_LAYOUT, height=310,
                               barmode='overlay', xaxis_title="Age",
                               yaxis_title="Count")
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Heatmap: Job Sat vs WLB ──
    st.markdown("### Attrition Heatmap — Job Satisfaction × Work-Life Balance")
    pivot = df_raw.groupby(['Job Satisfaction', 'Work-Life Balance'])['Attrition'].apply(
        lambda x: round((x == 'Left').mean() * 100, 1)).unstack()
    order_js  = ['Very High', 'High', 'Medium', 'Low']
    order_wlb = ['Excellent', 'Good', 'Fair', 'Poor']
    pivot = pivot.reindex(index=order_js, columns=order_wlb, fill_value=0)

    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale='RdYlGn_r',
        text=[[f"{v:.1f}%" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        hovertemplate="Job Sat: %{y}<br>WLB: %{x}<br>Attrition: %{z:.1f}%<extra></extra>"
    ))
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=280,
                           xaxis_title="Work-Life Balance",
                           yaxis_title="Job Satisfaction")
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 2 — SINGLE PREDICTION
# ══════════════════════════════════════════════════════════════
elif page == "🔮  Single Prediction":
    st.markdown("# Single Employee Prediction")
    st.markdown("<p class='subtitle'>Enter an employee's profile and get instant attrition probability</p>", unsafe_allow_html=True)

    with st.form("predict_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("#### 👤 Personal")
            age        = st.slider("Age", 18, 65, 35)
            gender     = st.selectbox("Gender",         CAT_OPTIONS['Gender'])
            marital    = st.selectbox("Marital Status", CAT_OPTIONS['Marital Status'])
            dependents = st.number_input("Number of Dependents", 0, 10, 2)
            education  = st.selectbox("Education Level", CAT_OPTIONS['Education Level'])
            distance   = st.slider("Distance from Home (km)", 1, 60, 15)

        with c2:
            st.markdown("#### 💼 Job Details")
            job_role   = st.selectbox("Job Role",     CAT_OPTIONS['Job Role'])
            job_level  = st.selectbox("Job Level",    CAT_OPTIONS['Job Level'])
            income     = st.number_input("Monthly Income ($)", 1000, 20000, 5000, step=500)
            yrs_co     = st.slider("Years at Company", 0, 40, 5)
            promotions = st.number_input("Number of Promotions", 0, 15, 1)
            overtime   = st.selectbox("Overtime", CAT_OPTIONS['Overtime'])
            co_tenure  = st.slider("Company Tenure (years)", 0, 40, 8)

        with c3:
            st.markdown("#### 🌱 Work Culture")
            wlb        = st.selectbox("Work-Life Balance",        CAT_OPTIONS['Work-Life Balance'])
            job_sat    = st.selectbox("Job Satisfaction",         CAT_OPTIONS['Job Satisfaction'])
            perf       = st.selectbox("Performance Rating",       CAT_OPTIONS['Performance Rating'])
            remote     = st.selectbox("Remote Work",              CAT_OPTIONS['Remote Work'])
            leadership = st.selectbox("Leadership Opportunities", CAT_OPTIONS['Leadership Opportunities'])
            innovation = st.selectbox("Innovation Opportunities", CAT_OPTIONS['Innovation Opportunities'])
            co_rep     = st.selectbox("Company Reputation",       CAT_OPTIONS['Company Reputation'])
            recognition= st.selectbox("Employee Recognition",     CAT_OPTIONS['Employee Recognition'])
            co_size    = st.selectbox("Company Size",             CAT_OPTIONS['Company Size'])

        submitted = st.form_submit_button("⚡ Predict Attrition Risk", use_container_width=True)

    if submitted:
        row = {
            'Age': age, 'Gender': gender, 'Years at Company': yrs_co,
            'Job Role': job_role, 'Monthly Income': income,
            'Work-Life Balance': wlb, 'Job Satisfaction': job_sat,
            'Performance Rating': perf, 'Number of Promotions': promotions,
            'Overtime': overtime, 'Distance from Home': distance,
            'Education Level': education, 'Marital Status': marital,
            'Number of Dependents': dependents, 'Job Level': job_level,
            'Company Size': co_size, 'Company Tenure': co_tenure,
            'Remote Work': remote, 'Leadership Opportunities': leadership,
            'Innovation Opportunities': innovation,
            'Company Reputation': co_rep, 'Employee Recognition': recognition,
        }

        with st.spinner("Running inference..."):
            time.sleep(0.4)
            p_left, p_stayed = predict_single(model, row)

        # ── Result card ──
        risk_level = "🔴 HIGH RISK" if p_left > 0.65 else ("🟡 MODERATE RISK" if p_left > 0.40 else "🟢 LOW RISK")
        alert_cls  = "alert-high" if p_left > 0.65 else ("alert-medium" if p_left > 0.40 else "alert-low")
        accent_col = "#ef4444" if p_left > 0.65 else ("#f97316" if p_left > 0.40 else "#10b981")

        st.markdown(f"""
        <div class='risk-card {alert_cls}' style='border-radius:16px;padding:1.8rem;margin-top:1rem;'>
          <div style='font-size:.75rem;letter-spacing:.1em;color:#8888a8;margin-bottom:.5rem;'>ATTRITION RISK ASSESSMENT</div>
          <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;'>
            <div>
              <div style='font-size:2.8rem;font-weight:800;color:{accent_col};'>{p_left*100:.1f}%</div>
              <div style='font-size:1rem;font-weight:600;color:{accent_col};margin-top:.2rem;'>{risk_level}</div>
              <div style='font-size:.82rem;color:#8888a8;margin-top:.4rem;'>
                Probability of leaving: <b style='color:{accent_col};'>{p_left*100:.1f}%</b> &nbsp;·&nbsp;
                Probability of staying: <b style='color:#10b981;'>{p_stayed*100:.1f}%</b>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=p_left * 100,
            title=dict(text="Attrition Probability (%)", font=dict(size=14, color='#8888a8')),
            delta=dict(reference=50, increasing=dict(color="#ef4444"), decreasing=dict(color="#10b981")),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor='#8888a8'),
                bar=dict(color=accent_col),
                bgcolor='rgba(18,18,26,0.8)',
                steps=[
                    dict(range=[0, 40],   color='rgba(16,185,129,.18)'),
                    dict(range=[40, 65],  color='rgba(249,115,22,.18)'),
                    dict(range=[65, 100], color='rgba(239,68,68,.18)'),
                ],
                threshold=dict(line=dict(color='white', width=2), thickness=.75, value=p_left*100)
            )
        ))
        fig_gauge.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Feature importance mini-bar for this employee context
        st.markdown("### Top Influencing Factors (Global Feature Importance)")
        fi = dict(zip(FEATURES, model.feature_importances_))
        fi_df = pd.DataFrame(sorted(fi.items(), key=lambda x: x[1], reverse=True)[:10],
                             columns=['Feature', 'Importance'])
        fig_fi = go.Figure(go.Bar(
            x=fi_df['Importance'], y=fi_df['Feature'], orientation='h',
            marker=dict(color=fi_df['Importance'],
                        colorscale=[[0,'#5b46e0'],[1,'#a78bfa']], showscale=False),
            text=[f"{v:.3f}" for v in fi_df['Importance']],
            textposition='outside'
        ))
        fig_fi.update_layout(**PLOTLY_LAYOUT, height=380, xaxis=dict(visible=False),
                             yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_fi, use_container_width=True)

        # Recommendations
        st.markdown("### 💡 AI Recommendations")
        recs = []
        if overtime == "Yes":         recs.append("⚠️ **Overtime detected** — High overtime is a strong attrition predictor. Consider workload rebalancing.")
        if wlb in ['Fair', 'Poor']:   recs.append("⚠️ **Work-Life Balance is low** — Flexible hours or remote-first policies may help retention.")
        if job_sat in ['Low', 'Medium']: recs.append("⚠️ **Low job satisfaction** — Schedule a 1-on-1 review to understand pain points.")
        if promotions == 0:           recs.append("💼 **No promotions recorded** — Career development conversations are overdue.")
        if remote == "No":            recs.append("🏠 **No remote work option** — Offering hybrid flexibility reduces attrition significantly.")
        if recognition in ['Low']:    recs.append("🏆 **Low employee recognition** — Implement recognition programs to boost morale.")
        if not recs:                  recs.append("✅ **All indicators look positive** — Continue maintaining this employee's engagement.")

        for r in recs:
            st.markdown(f"> {r}")


# ══════════════════════════════════════════════════════════════
#  PAGE 3 — BATCH ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "📦  Batch Analysis":
    st.markdown("# Batch Attrition Analysis")
    st.markdown("<p class='subtitle'>Upload a CSV or use the preloaded dataset for bulk predictions</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📁 Upload Custom CSV", "🗃️ Use Preloaded Dataset"])

    with tab1:
        uploaded = st.file_uploader("Upload employee CSV (must match feature schema)", type=['csv'])
        if uploaded:
            df_up = pd.read_csv(uploaded)
            st.success(f"Loaded {len(df_up):,} rows.")
            if all(f in df_up.columns for f in FEATURES):
                X_up = preprocess(df_up)
                probs = model.predict_proba(X_up)[:, 1]
                df_up['Attrition_Probability'] = probs
                df_up['Risk_Level'] = pd.cut(probs, bins=[0, .4, .65, 1.0],
                                             labels=['Low', 'Moderate', 'High'])
                st.dataframe(df_up[['Attrition_Probability', 'Risk_Level'] + FEATURES[:6]].head(50),
                             use_container_width=True)
                csv_out = df_up.to_csv(index=False).encode()
                st.download_button("⬇️ Download Results CSV", csv_out, "attrition_results.csv", "text/csv")
            else:
                st.error("CSV missing required feature columns.")

    with tab2:
        sample_n = st.slider("Sample size for analysis", 500, len(df_raw), 2000, step=500)
        df_sample = df_raw.sample(sample_n, random_state=42).reset_index(drop=True)
        X_samp = preprocess(df_sample)
        probs_samp = model.predict_proba(X_samp)[:, 1]
        df_sample['Risk_Score'] = probs_samp
        df_sample['Risk_Level'] = pd.cut(probs_samp, bins=[0, .4, .65, 1.0],
                                         labels=['Low', 'Moderate', 'High'])

        c1, c2, c3 = st.columns(3)
        c1.metric("High Risk",   f"{(probs_samp > .65).sum():,}", f"{(probs_samp>.65).mean()*100:.1f}%")
        c2.metric("Moderate",    f"{((probs_samp>.4)&(probs_samp<=.65)).sum():,}")
        c3.metric("Low Risk",    f"{(probs_samp <= .4).sum():,}")

        # Risk distribution histogram
        fig_rdist = go.Figure(go.Histogram(
            x=probs_samp * 100, nbinsx=40,
            marker=dict(color=probs_samp * 100,
                        colorscale=[[0,'#10b981'],[0.5,'#f97316'],[1,'#ef4444']],
                        showscale=True, colorbar=dict(title='%')),
            hovertemplate="Risk: %{x:.1f}%<br>Count: %{y}<extra></extra>"
        ))
        fig_rdist.update_layout(**PLOTLY_LAYOUT, height=300,
                                title="Risk Score Distribution",
                                xaxis_title="Attrition Probability (%)",
                                yaxis_title="Employee Count")
        st.plotly_chart(fig_rdist, use_container_width=True)

        # Top-20 highest risk
        st.markdown("### 🚨 Top 20 Highest-Risk Employees")
        top20 = df_sample.nlargest(20, 'Risk_Score')[
            ['Employee ID', 'Age', 'Job Role', 'Job Level', 'Monthly Income',
             'Years at Company', 'Risk_Score', 'Risk_Level']
        ].reset_index(drop=True)
        top20['Risk_Score'] = top20['Risk_Score'].apply(lambda x: f"{x*100:.1f}%")
        st.dataframe(top20, use_container_width=True)

        # Download
        csv_dl = df_sample.to_csv(index=False).encode()
        st.download_button("⬇️ Download Full Sample Results", csv_dl, "batch_results.csv", "text/csv")


# ══════════════════════════════════════════════════════════════
#  PAGE 4 — MODEL INSIGHTS
# ══════════════════════════════════════════════════════════════
elif page == "📊  Model Insights":
    st.markdown("# Model Insights & Performance")
    st.markdown("<p class='subtitle'>Deep-dive into model accuracy, AUC-ROC, confusion matrix, and feature importance</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Performance Metrics", "🔍 Feature Importance", "📉 ROC & PR Curves"])

    with tab1:
        cr = classification_report(y_true, y_pred, output_dict=True)
        cm = confusion_matrix(y_true, y_pred)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Accuracy",  f"{acc*100:.2f}%")
        c2.metric("AUC-ROC",   f"{auc:.4f}")
        c3.metric("Precision (Left)", f"{cr['1']['precision']*100:.1f}%")
        c4.metric("Recall (Left)",    f"{cr['1']['recall']*100:.1f}%")

        # Confusion Matrix
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=['Predicted Stayed', 'Predicted Left'],
            y=['Actual Stayed', 'Actual Left'],
            colorscale=[[0,'#12121a'],[1,'#7c6af7']],
            text=cm.astype(str), texttemplate='<b>%{text}</b>',
            textfont=dict(size=18),
            hovertemplate="%{y} → %{x}: %{z}<extra></extra>"
        ))
        fig_cm.update_layout(**PLOTLY_LAYOUT, height=380, title="Confusion Matrix")
        st.plotly_chart(fig_cm, use_container_width=True)

        # Classification report table
        st.markdown("#### Detailed Classification Report")
        cr_df = pd.DataFrame({
            'Class':     ['Stayed (0)', 'Left (1)', 'Macro Avg', 'Weighted Avg'],
            'Precision': [cr['0']['precision'], cr['1']['precision'], cr['macro avg']['precision'], cr['weighted avg']['precision']],
            'Recall':    [cr['0']['recall'],    cr['1']['recall'],    cr['macro avg']['recall'],    cr['weighted avg']['recall']],
            'F1-Score':  [cr['0']['f1-score'],  cr['1']['f1-score'],  cr['macro avg']['f1-score'],  cr['weighted avg']['f1-score']],
            'Support':   [cr['0']['support'],   cr['1']['support'],   cr['macro avg']['support'],   cr['weighted avg']['support']],
        })
        cr_df[['Precision','Recall','F1-Score']] = cr_df[['Precision','Recall','F1-Score']].applymap(lambda x: f"{x:.4f}")
        st.dataframe(cr_df, use_container_width=True, hide_index=True)

    with tab2:
        fi = dict(zip(FEATURES, model.feature_importances_))
        fi_df = pd.DataFrame(sorted(fi.items(), key=lambda x: x[1], reverse=True),
                             columns=['Feature', 'Importance'])

        fig_fi_full = go.Figure(go.Bar(
            x=fi_df['Importance'], y=fi_df['Feature'], orientation='h',
            marker=dict(
                color=fi_df['Importance'],
                colorscale=[[0,'#2d2460'],[0.5,'#7c6af7'],[1,'#c4b5fd']],
                showscale=True, colorbar=dict(title='Importance')
            ),
            text=[f"{v:.4f}" for v in fi_df['Importance']],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>"
        ))
        fig_fi_full.update_layout(
            **PLOTLY_LAYOUT, height=580,
            title="Feature Importance (All 22 Features)",
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(autorange='reversed')
        )
        st.plotly_chart(fig_fi_full, use_container_width=True)

        # Treemap view
        fig_tree = px.treemap(
            fi_df, path=['Feature'], values='Importance',
            color='Importance', color_continuous_scale=['#12121a','#7c6af7','#c4b5fd'],
            title="Feature Importance Treemap"
        )
        fig_tree.update_layout(**PLOTLY_LAYOUT, height=400)
        fig_tree.update_traces(textinfo='label+value', textfont=dict(size=12))
        st.plotly_chart(fig_tree, use_container_width=True)

    with tab3:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        prec, rec, _ = precision_recall_curve(y_true, y_prob)

        col_l, col_r = st.columns(2)
        with col_l:
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC (AUC={auc:.3f})',
                                         line=dict(color='#7c6af7', width=2.5)))
            fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines',
                                         line=dict(color='#555', dash='dash', width=1), name='Random'))
            fig_roc.update_layout(**PLOTLY_LAYOUT, height=360, title="ROC Curve",
                                  xaxis_title="False Positive Rate",
                                  yaxis_title="True Positive Rate")
            st.plotly_chart(fig_roc, use_container_width=True)

        with col_r:
            baseline = y_true.mean()
            fig_pr = go.Figure()
            fig_pr.add_trace(go.Scatter(x=rec, y=prec, mode='lines', name='PR Curve',
                                         line=dict(color='#f97316', width=2.5)))
            fig_pr.add_hline(y=baseline, line_dash='dash', line_color='#555',
                              annotation_text="Baseline", annotation_position="top right")
            fig_pr.update_layout(**PLOTLY_LAYOUT, height=360, title="Precision-Recall Curve",
                                  xaxis_title="Recall", yaxis_title="Precision")
            st.plotly_chart(fig_pr, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 5 — RISK PROFILER
# ══════════════════════════════════════════════════════════════
elif page == "🎯  Risk Profiler":
    st.markdown("# Risk Profiler")
    st.markdown("<p class='subtitle'>Segment employees by risk tier and identify retention leverage points</p>", unsafe_allow_html=True)

    # Compute risk on full dataset
    df_risk = df_raw.copy()
    df_risk['Risk_Score'] = y_prob
    df_risk['Risk_Level'] = pd.cut(y_prob, bins=[0, .4, .65, 1.0],
                                    labels=['Low', 'Moderate', 'High'])

    # ── Risk tier summary ──
    tier_counts = df_risk['Risk_Level'].value_counts()
    c1, c2, c3 = st.columns(3)
    for col, (tier, color, emoji) in zip([c1,c2,c3], [
        ('High','#ef4444','🔴'), ('Moderate','#f97316','🟡'), ('Low','#10b981','🟢')
    ]):
        cnt = tier_counts.get(tier, 0)
        col.markdown(f"""
        <div style='background:var(--bg-card);border:1px solid {color}40;border-radius:16px;
                    padding:1.2rem;text-align:center;'>
          <div style='font-size:2rem;'>{emoji}</div>
          <div style='font-size:1.8rem;font-weight:800;color:{color};'>{cnt:,}</div>
          <div style='font-size:.8rem;color:#8888a8;letter-spacing:.06em;text-transform:uppercase;'>{tier} Risk</div>
          <div style='font-size:.9rem;color:#ccc;margin-top:.3rem;'>{cnt/len(df_risk)*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Segment analysis ──
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### Risk by Marital Status")
        ms_risk = df_risk.groupby('Marital Status')['Risk_Score'].mean().reset_index()
        ms_risk.columns = ['Marital Status', 'Avg Risk']
        ms_risk = ms_risk.sort_values('Avg Risk', ascending=False)
        fig_ms = go.Figure(go.Bar(
            x=ms_risk['Marital Status'], y=ms_risk['Avg Risk'] * 100,
            marker_color=['#ef4444','#f97316','#10b981'][:len(ms_risk)],
            text=[f"{v*100:.1f}%" for v in ms_risk['Avg Risk']],
            textposition='outside'
        ))
        fig_ms.update_layout(**PLOTLY_LAYOUT, height=280, yaxis_title="Avg Risk Score (%)")
        st.plotly_chart(fig_ms, use_container_width=True)

    with col_r:
        st.markdown("### Risk by Job Level")
        jl_risk = df_risk.groupby('Job Level')['Risk_Score'].mean().reset_index()
        jl_risk.columns = ['Job Level', 'Avg Risk']
        jl_risk = jl_risk.sort_values('Avg Risk', ascending=False)
        fig_jl = go.Figure(go.Bar(
            x=jl_risk['Job Level'], y=jl_risk['Avg Risk'] * 100,
            marker_color=['#7c6af7','#a78bfa','#c4b5fd'][:len(jl_risk)],
            text=[f"{v*100:.1f}%" for v in jl_risk['Avg Risk']],
            textposition='outside'
        ))
        fig_jl.update_layout(**PLOTLY_LAYOUT, height=280, yaxis_title="Avg Risk Score (%)")
        st.plotly_chart(fig_jl, use_container_width=True)

    # ── Scatter: Income vs Risk ──
    st.markdown("### Income vs Attrition Risk (Sample 1000)")
    df_scat = df_risk.sample(min(1000, len(df_risk)), random_state=7)
    fig_scat = px.scatter(
        df_scat, x='Monthly Income', y='Risk_Score',
        color='Risk_Level',
        color_discrete_map={'High':'#ef4444','Moderate':'#f97316','Low':'#10b981'},
        hover_data=['Age', 'Job Role', 'Job Level'],
        labels={'Risk_Score': 'Attrition Probability', 'Monthly Income': 'Monthly Income ($)'},
        opacity=0.65
    )
    fig_scat.update_traces(marker=dict(size=7))
    fig_scat.update_layout(**PLOTLY_LAYOUT, height=380)
    st.plotly_chart(fig_scat, use_container_width=True)

    # ── Risk + Overtime breakdown ──
    st.markdown("### Risk Level vs Overtime Status")
    ov_risk = df_risk.groupby(['Overtime', 'Risk_Level']).size().reset_index(name='Count')
    fig_ov = px.bar(ov_risk, x='Overtime', y='Count', color='Risk_Level',
                    color_discrete_map={'High':'#ef4444','Moderate':'#f97316','Low':'#10b981'},
                    barmode='group')
    fig_ov.update_layout(**PLOTLY_LAYOUT, height=320)
    st.plotly_chart(fig_ov, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 6 — DATA EXPLORER
# ══════════════════════════════════════════════════════════════
elif page == "📋  Data Explorer":
    st.markdown("# Data Explorer")
    st.markdown("<p class='subtitle'>Interactively filter and explore the employee dataset</p>", unsafe_allow_html=True)

    # ── Filters ──
    with st.expander("🔧 Filters", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        sel_role    = c1.multiselect("Job Role",        df_raw['Job Role'].unique(),   default=list(df_raw['Job Role'].unique()))
        sel_level   = c2.multiselect("Job Level",       df_raw['Job Level'].unique(),  default=list(df_raw['Job Level'].unique()))
        sel_att     = c3.multiselect("Attrition",       df_raw['Attrition'].unique(),  default=list(df_raw['Attrition'].unique()))
        income_rng  = c4.slider("Monthly Income Range ($)",
                                int(df_raw['Monthly Income'].min()),
                                int(df_raw['Monthly Income'].max()),
                                (1500, 12000))

    df_filt = df_raw[
        df_raw['Job Role'].isin(sel_role) &
        df_raw['Job Level'].isin(sel_level) &
        df_raw['Attrition'].isin(sel_att) &
        df_raw['Monthly Income'].between(*income_rng)
    ]

    st.markdown(f"**{len(df_filt):,}** employees match your filters")

    # ── Quick stats ──
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Age",    f"{df_filt['Age'].mean():.1f}")
    c2.metric("Avg Income", f"${df_filt['Monthly Income'].mean():,.0f}")
    c3.metric("Avg Tenure", f"{df_filt['Years at Company'].mean():.1f} yrs")

    # ── Column selector ──
    cols_show = st.multiselect(
        "Select columns to display",
        df_raw.columns.tolist(),
        default=['Employee ID', 'Age', 'Gender', 'Job Role', 'Job Level',
                 'Monthly Income', 'Years at Company', 'Attrition']
    )
    st.dataframe(df_filt[cols_show].reset_index(drop=True), use_container_width=True, height=400)

    # ── Correlation heatmap ──
    st.markdown("### Numeric Feature Correlation Matrix")
    num_df = df_filt[NUM_COLS + ['Monthly Income']].copy()
    corr = num_df.corr()
    fig_corr = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        hovertemplate="%{y} × %{x}: %{z:.3f}<extra></extra>"
    ))
    fig_corr.update_layout(**PLOTLY_LAYOUT, height=420)
    st.plotly_chart(fig_corr, use_container_width=True)

    # ── Pairplot matrix (Income, Age, Tenure, Distance) ──
    st.markdown("### Key Variable Distributions")
    fig_pair = make_subplots(rows=1, cols=4,
                             subplot_titles=['Monthly Income', 'Age', 'Years at Company', 'Distance from Home'])
    pair_vars = ['Monthly Income', 'Age', 'Years at Company', 'Distance from Home']
    colors_att = {'Stayed': '#10b981', 'Left': '#ef4444'}
    for i, var in enumerate(pair_vars, 1):
        for att_val, col in colors_att.items():
            vals = df_filt[df_filt['Attrition'] == att_val][var]
            fig_pair.add_trace(go.Histogram(x=vals, name=att_val, marker_color=col,
                                             opacity=0.65, nbinsx=20,
                                             showlegend=(i == 1)), row=1, col=i)
    fig_pair.update_layout(**PLOTLY_LAYOUT, height=280, barmode='overlay')
    st.plotly_chart(fig_pair, use_container_width=True)

    # Download filtered
    csv_filt = df_filt.to_csv(index=False).encode()
    st.download_button("⬇️ Download Filtered Data", csv_filt, "filtered_employees.csv", "text/csv")