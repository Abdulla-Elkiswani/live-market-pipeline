import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px

# Configuration
DATA_URL = "https://github.com/Abdulla-Elkiswani/live-market-pipeline/releases/download/v1.0.0/market_data.parquet"

st.set_page_config(page_title="Market Data Gateway", layout="wide")
st.title("Market Data Gateway: Production Monitor")

# 1. Data Loading Logic


@st.cache_data(ttl=600)
def load_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_parquet(io.BytesIO(response.content))

# 2. Data Validation Guardrails


def validate_data(df):
    """Ensures data integrity before the app renders."""
    required_columns = {'job_title', 'salary_eur', 'country'}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Data Schema Mismatch! Missing columns: {required_columns - set(df.columns)}")

    if (df['salary_eur'] < 0).any():
        raise ValueError(
            "Data Integrity Error: Negative salary values detected.")

    return True


# Main Execution Flow
try:
    df = load_data(DATA_URL)
    validate_data(df)

    # Sidebar: Filters
    st.sidebar.header("Filters")
    countries = st.sidebar.multiselect(
        "Select Countries",
        options=df['country'].unique(),
        default=df['country'].unique()
    )

    # Filter data
    filtered_df = df[df['country'].isin(countries)]

    # Dashboard Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Jobs Monitored", len(filtered_df))
    col2.metric("Average Salary", f"€{filtered_df['salary_eur'].mean():,.0f}")

    # Visuals
    st.subheader("Salary Distribution by Job Title")
    fig = px.bar(filtered_df, x='job_title', y='salary_eur',
                 color='country', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # Data Table
    st.subheader("Raw Data")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"System Operational Error: {e}")
    st.stop()
