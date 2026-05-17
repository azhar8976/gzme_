
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(layout='wide')

st.title('Movie Vote Average Prediction App')

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\ak859\Downloads\mymoviedb.csv", lineterminator='\n')
    return df

@st.cache_data
def preprocess_data(df):
    # Deep copy to avoid modifying original cached DataFrame
    df_processed = df.copy()

    # Correctly process 'Release_Date': Convert to datetime then extract year
    df_processed['Release_Date'] = pd.to_datetime(df_processed['Release_Date'], errors='coerce')
    df_processed['Release_Date'] = df_processed['Release_Date'].dt.year

    # Drop specified columns
    cols_to_drop = ["Overview", "Original_Language", "Poster_Url"]
    df_processed.drop(cols_to_drop, axis=1, inplace=True)

    # Define categorization function (as seen in the notebook)
    def catigorize_col(df_func, col, labels):
        # Handle cases where min/max might be NaN if all values are NaN after coerce
        if df_func[col].isnull().all():
            return df_func # Return df as is if column is all null

        desc_stats = df_func[col].describe()
        edges = [
            desc_stats['min'],
            desc_stats['25%'],
            desc_stats['50%'],
            desc_stats['75%'],
            desc_stats['max']
        ]
        # Adjust bins to ensure unique values for pd.cut, especially if many values are the same
        # Add a tiny epsilon to the max to ensure the max value is included if it's the only one at the boundary
        unique_edges = sorted(list(set(edges)))
        if len(unique_edges) < 2:
            # If not enough unique edges, fall back to a simpler categorization or handle as unique category
            df_func[col] = pd.Categorical(df_func[col].astype(str), categories=labels)
        else:
            # Ensure bins are strictly increasing
            bins_to_use = [unique_edges[0] - 0.01] + unique_edges[1:] # Adjust min bin to include actual min
            if len(bins_to_use) < len(labels) + 1: # If not enough bins for labels, adjust
                # This is a simplification; a more robust solution would dynamically create labels or merge bins
                bins_to_use = np.linspace(min(edges), max(edges) + 0.01, len(labels) + 1)

            df_func[col] = pd.cut(
                df_func[col],
                bins=bins_to_use,
                labels=labels[:len(bins_to_use)-1],
                duplicates='drop',
                include_lowest=True
            )
        return df_func

    # Apply categorization to 'Vote_Count'
    labels = ['not_popular', 'below_avg', 'average', 'popular']
    df_processed = catigorize_col(df_processed, 'Vote_Count', labels)

    # Process 'Genre' column: split, explode, and convert to category
    df_processed['Genre'] = df_processed['Genre'].str.split(', ')
    df_processed = df_processed.explode('Genre')
    df_processed['Genre'] = df_processed['Genre'].str.strip()
    df_processed = df_processed[df_processed['Genre'] != ''].reset_index(drop=True)
    df_processed['Genre'] = df_processed['Genre'].astype('category')

    # One-hot encode categorical features: 'Genre' and 'Vote_Count'
    df_encoded = pd.get_dummies(df_processed, columns=['Genre', 'Vote_Count'], drop_first=True)

    # Remove 'Title' if it's still present before splitting features/target
    if 'Title' in df_encoded.columns:
        df_encoded = df_encoded.drop('Title', axis=1)

    # Remove rows with NaN in the target variable or features after one-hot encoding
    df_encoded = df_encoded.dropna(subset=['Vote_Average'])

    return df_encoded

@st.cache_resource
def train_models(df_encoded):
    X = df_encoded.drop('Vote_Average', axis=1)
    y = df_encoded['Vote_Average']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    st.write("Training RandomForestRegressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    mae_rf, mse_rf, rmse_rf, r2_rf = evaluate_model(y_test, y_pred_rf)

    st.write("Training LinearRegression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    mae_lr, mse_lr, rmse_lr, r2_lr = evaluate_model(y_test, y_pred_lr)

    st.write("Training GradientBoostingRegressor...")
    gb_model = GradientBoostingRegressor(random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    mae_gb, mse_gb, rmse_gb, r2_gb = evaluate_model(y_test, y_pred_gb)

    return {
        'RandomForest': {'model': rf_model, 'preds': y_pred_rf, 'metrics': {'MAE': mae_rf, 'MSE': mse_rf, 'RMSE': rmse_rf, 'R2': r2_rf}},
        'LinearRegression': {'model': lr_model, 'preds': y_pred_lr, 'metrics': {'MAE': mae_lr, 'MSE': mse_lr, 'RMSE': rmse_lr, 'R2': r2_lr}},
        'GradientBoosting': {'model': gb_model, 'preds': y_pred_gb, 'metrics': {'MAE': mae_gb, 'MSE': mse_gb, 'RMSE': rmse_gb, 'R2': r2_gb}}
    }, X_test, y_test

def evaluate_model(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return mae, mse, rmse, r2

# Load and preprocess data
with st.spinner('Loading and preprocessing data...'):
    original_df = load_data()
    preprocessed_df = preprocess_data(original_df.copy())

# Train models
with st.spinner('Training models... This might take a moment.'):
    models_results, X_test, y_test = train_models(preprocessed_df.copy())

st.header("Model Performance Comparison")
metrics_data = {}
for name, result in models_results.items():
    metrics_data[name] = result['metrics']

metrics_df = pd.DataFrame.from_dict(metrics_data, orient='index')
st.dataframe(metrics_df)

st.header("Visualize Predictions")
model_choice = st.selectbox(
    'Choose a model to visualize its predictions:',
    ('RandomForest', 'LinearRegression', 'GradientBoosting')
)

if model_choice:
    selected_results = models_results[model_choice]
    y_pred_selected = selected_results['preds']

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.regplot(x=y_test, y=y_pred_selected, scatter_kws={'alpha':0.3}, line_kws={'color':'red'}, ax=ax)
    ax.set_xlabel('Actual Vote Average')
    ax.set_ylabel(f'Predicted Vote Average ({model_choice})')
    ax.set_title(f'Actual vs. Predicted Vote Average ({model_choice})')
    ax.grid(True)
    st.pyplot(fig)

st.markdown("--- ")
st.write("Data Preview after Preprocessing:")
st.dataframe(preprocessed_df.head())

st.sidebar.header("About")
st.sidebar.info(
    "This app demonstrates the prediction of movie vote averages using various machine learning models." 
    "Data is loaded, preprocessed, and models are trained directly within the app." 
    "You can compare model performance and visualize predictions." 
)