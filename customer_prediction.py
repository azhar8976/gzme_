# import streamlit as st
# import pandas as pd
# import numpy as np

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import LabelEncoder

# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.figure_factory as ff

# # ==========================================
# # PAGE CONFIG
# # ==========================================

# st.set_page_config(
#     page_title="AI Customer Churn Dashboard",
#     page_icon="🚀",
#     layout="wide"
# )

# # ==========================================
# # CUSTOM CSS
# # ==========================================

# st.markdown("""
# <style>

# .stApp{
# background: linear-gradient(
# 135deg,
# #0f172a,
# #111827,
# #1e293b
# );
# color:white;
# }

# h1,h2,h3{
# color:#00FFFF;
# }

# [data-testid="stSidebar"]{
# background:#111827;
# }

# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # TITLE
# # ==========================================

# st.title("🚀 AI Customer Churn Prediction Dashboard")

# # ==========================================
# # LOAD DATA
# # ==========================================

# try:
#     df = pd.read_csv(
#         "customer_churn_random_forest_dataset-1 (1).csv"
#     )
# except Exception as e:
#     st.error(f"CSV Error: {e}")
#     st.stop()

# # ==========================================
# # ENCODE GENDER
# # ==========================================

# if "Gender" in df.columns:
#     le = LabelEncoder()
#     df["Gender"] = le.fit_transform(df["Gender"])

# # ==========================================
# # FEATURES & TARGET
# # ==========================================

# target_col = "Churn"

# X = df.drop(
#     ["CustomerID", target_col],
#     axis=1
# )

# y = df[target_col]

# # ==========================================
# # TRAIN TEST SPLIT
# # ==========================================

# X_train, X_test, y_train, y_test = train_test_split(
#     X,
#     y,
#     test_size=0.2,
#     random_state=42
# )

# # ==========================================
# # RANDOM FOREST MODEL
# # ==========================================

# model = RandomForestClassifier(
#     n_estimators=300,
#     random_state=42
# )

# model.fit(X_train, y_train)

# pred = model.predict(X_test)

# accuracy = accuracy_score(
#     y_test,
#     pred
# )

# # ==========================================
# # KPI CARDS
# # ==========================================

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric(
#         "Accuracy",
#         f"{accuracy:.2%}"
#     )

# with col2:
#     st.metric(
#         "Customers",
#         len(df)
#     )

# with col3:
#     st.metric(
#         "Churn Rate",
#         f"{df[target_col].mean()*100:.2f}%"
#     )

# with col4:
#     st.metric(
#         "Features",
#         len(X.columns)
#     )

# # ==========================================
# # SIDEBAR
# # ==========================================

# st.sidebar.header("Customer Information")

# credit_score = st.sidebar.slider(
#     "Credit Score",
#     300,
#     900,
#     650
# )

# gender = st.sidebar.selectbox(
#     "Gender",
#     [0,1]
# )

# age = st.sidebar.slider(
#     "Age",
#     18,
#     90,
#     35
# )

# tenure = st.sidebar.slider(
#     "Tenure",
#     0,
#     10,
#     5
# )

# balance = st.sidebar.number_input(
#     "Balance",
#     value=50000.0
# )

# products = st.sidebar.slider(
#     "Products",
#     1,
#     4,
#     2
# )

# active = st.sidebar.selectbox(
#     "Active Member",
#     [0,1]
# )

# salary = st.sidebar.number_input(
#     "Estimated Salary",
#     value=100000.0
# )

# # ==========================================
# # PREDICTION
# # ==========================================

# if st.sidebar.button("Predict Churn"):

#     sample = pd.DataFrame({
#         "Gender":[gender],
#         "Age":[age],
#         "Tenure":[tenure],
#         "Balance":[balance],
#         "Products":[products],
#         "CreditScore":[credit_score],
#         "ActiveMember":[active],
#         "EstimatedSalary":[salary]
#     })

#     prediction = model.predict(sample)[0]
#     probability = model.predict_proba(sample)[0][1]

#     st.subheader("Prediction Result")

#     if prediction == 1:

#         st.error(
#             f"⚠ Customer likely to Churn ({probability:.2%})"
#         )

#     else:

#         st.success(
#             f"✅ Customer likely to Stay ({1-probability:.2%})"
#         )

#     # Gauge Meter

#     gauge = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=probability*100,
#         title={"text":"Customer Churn Risk %"},
#         gauge={
#             "axis":{"range":[0,100]}
#         }
#     ))

#     st.plotly_chart(
#         gauge,
#         use_container_width=True
#     )

# # ==========================================
# # TABS
# # ==========================================

# tab1, tab2, tab3, tab4 = st.tabs([
#     "📊 Dashboard",
#     "📈 Analytics",
#     "🌐 3D Visualization",
#     "📂 Dataset"
# ])

# # ==========================================
# # TAB 1
# # ==========================================

# with tab1:

#     st.subheader("Customer Churn Distribution")

#     fig1 = px.histogram(
#         df,
#         x="Churn",
#         color="Churn",
#         template="plotly_dark"
#     )

#     st.plotly_chart(
#         fig1,
#         use_container_width=True
#     )

#     st.subheader("Customer Segmentation")

#     pie = px.pie(
#         df,
#         names="Churn",
#         title="Customer Churn Segmentation"
#     )

#     st.plotly_chart(
#         pie,
#         use_container_width=True
#     )

# # ==========================================
# # TAB 2
# # ==========================================

# with tab2:

#     st.subheader("Feature Importance")

#     importance = pd.DataFrame({
#         "Feature": X.columns,
#         "Importance": model.feature_importances_
#     })

#     importance = importance.sort_values(
#         "Importance",
#         ascending=False
#     )

#     fig2 = px.bar(
#         importance,
#         x="Importance",
#         y="Feature",
#         orientation="h",
#         template="plotly_dark"
#     )

#     st.plotly_chart(
#         fig2,
#         use_container_width=True
#     )

#     st.subheader("Correlation Heatmap")

#     corr = df.select_dtypes(
#         include=np.number
#     ).corr()

#     heatmap = ff.create_annotated_heatmap(
#         z=corr.values,
#         x=list(corr.columns),
#         y=list(corr.index)
#     )

#     st.plotly_chart(
#         heatmap,
#         use_container_width=True
#     )

# # ==========================================
# # TAB 3
# # ==========================================

# with tab3:

#     st.subheader("3D Customer Visualization")

#     fig3 = px.scatter_3d(
#         df,
#         x="Age",
#         y="Balance",
#         z="CreditScore",
#         color="Churn",
#         size="EstimatedSalary",
#         template="plotly_dark"
#     )

#     st.plotly_chart(
#         fig3,
#         use_container_width=True
#     )

# # ==========================================
# # TAB 4
# # ==========================================

# with tab4:

#     st.subheader("Dataset Preview")

#     st.dataframe(df)

#     st.subheader("Dataset Shape")

#     st.write(df.shape)

# # ==========================================
# # AI INSIGHTS
# # ==========================================

# st.info(
# f"""
# 🤖 AI INSIGHTS

# • Total Customers : {len(df)}

# • Model Accuracy : {accuracy:.2%}

# • Churn Rate : {df[target_col].mean()*100:.2f}%

# • Most Important Feature :
# {X.columns[np.argmax(model.feature_importances_)]}

# • Random Forest Model Active
# """
# )








import streamlit as st
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>
.stApp{
    background-color:#0E1117;
    color:white;
}
h1,h2,h3{
    color:#00FFFF;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------

st.title("🚀 AI Customer Churn Prediction Dashboard")

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv(
    "customer_churn_random_forest_dataset-1 (1).csv"
)

# -------------------------
# SHOW COLUMNS
# -------------------------

st.write("Dataset Columns:")
st.write(df.columns.tolist())

# -------------------------
# RENAME COLUMNS IF NEEDED
# -------------------------

if "Products" in df.columns:
    df.rename(columns={"Products":"NumOfProducts"}, inplace=True)

if "ActiveMember" not in df.columns:
    if "IsActiveMember" in df.columns:
        df.rename(columns={"IsActiveMember":"ActiveMember"}, inplace=True)

# -------------------------
# ENCODE GENDER
# -------------------------

if "Gender" in df.columns:
    le = LabelEncoder()
    df["Gender"] = le.fit_transform(df["Gender"])

# -------------------------
# TARGET COLUMN CHECK
# -------------------------

target_col = None

for col in df.columns:
    if col.lower() == "churn":
        target_col = col
        break

if target_col is None:
    st.error("Churn column not found in dataset")
    st.stop()

# -------------------------
# FEATURES
# -------------------------

X = df.drop(target_col, axis=1)
y = df[target_col]

# -------------------------
# TRAIN TEST SPLIT
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -------------------------
# RANDOM FOREST MODEL
# -------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

# -------------------------
# ACCURACY
# -------------------------

st.metric(
    "Model Accuracy",
    f"{accuracy:.2%}"
)

# -------------------------
# SIDEBAR INPUTS
# -------------------------

st.sidebar.header("Customer Information")

credit_score = st.sidebar.slider(
    "Credit Score",
    300,
    900,
    650
)

gender = st.sidebar.selectbox(
    "Gender",
    [0,1]
)

age = st.sidebar.slider(
    "Age",
    18,
    90,
    35
)

tenure = st.sidebar.slider(
    "Tenure",
    0,
    10,
    5
)

balance = st.sidebar.number_input(
    "Balance",
    value=50000.0
)

products = st.sidebar.slider(
    "Num Of Products",
    1,
    4,
    2
)

active = st.sidebar.selectbox(
    "Active Member",
    [0,1]
)

salary = st.sidebar.number_input(
    "Estimated Salary",
    value=100000.0
)

# -------------------------
# PREDICTION
# -------------------------

if st.sidebar.button("Predict Churn"):

    sample = pd.DataFrame({
        "CreditScore":[credit_score],
        "Gender":[gender],
        "Age":[age],
        "Tenure":[tenure],
        "Balance":[balance],
        "NumOfProducts":[products],
        "ActiveMember":[active],
        "EstimatedSalary":[salary]
    })

    sample = sample.reindex(columns=X.columns, fill_value=0)

    prediction = model.predict(sample)[0]
    probability = model.predict_proba(sample)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error(
            f"⚠ Customer likely to Churn ({probability:.2%})"
        )
    else:
        st.success(
            f"✅ Customer likely to Stay ({1-probability:.2%})"
        )

# -------------------------
# CHURN DISTRIBUTION
# -------------------------

st.subheader("Customer Churn Distribution")

fig1 = px.histogram(
    df,
    x=target_col,
    color=target_col,
    template="plotly_dark"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -------------------------
# FEATURE IMPORTANCE
# -------------------------

st.subheader("Feature Importance")

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

fig2 = px.bar(
    importance,
    x="Importance",
    y="Feature",
    orientation="h",
    template="plotly_dark"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------
# 3D VISUALIZATION
# -------------------------

if (
    "Age" in df.columns and
    "Balance" in df.columns and
    "CreditScore" in df.columns
):

    st.subheader("3D Customer Visualization")

    fig3 = px.scatter_3d(
        df,
        x="Age",
        y="Balance",
        z="CreditScore",
        color=target_col,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# -------------------------
# DATASET PREVIEW
# -------------------------

st.subheader("Dataset Preview")

st.dataframe(df.head())

st.subheader("Dataset Shape")

st.write(df.shape)