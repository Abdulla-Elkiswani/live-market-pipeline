import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
import hashlib

# Configuration
DATA_URL = "https://github.com/Abdulla-Elkiswani/live-market-pipeline/releases/download/v1.0.0/market_data.parquet"
# This is the fingerprint of your file to ensure zero corruption during download
EXPECTED_HASH = "194667e22ccc70b1fd836566635739caf5b1df73506e5884fe7d7ac113739d4f"

st.set_page_config(page_title="Market Data Gateway", layout="wide")
st.title("Market Data Gateway: Production Monitor")

# 1. Secured Data Loading Logic


@st.cache_data(ttl=600)
def load_and_verify_data(url):
    response = requests.get(url)
    response.raise_for_status()
    content = response.content

    # Hash Verification
    actual_hash = hashlib.sha256(content).hexdigest()
    if actual_hash != EXPECTED_HASH:
        raise ValueError(
            f"Security Alert: Hash mismatch! Expected {EXPECTED_HASH}, got {actual_hash}")

    return pd.read_parquet(io.BytesIO(content))

# 2. Data Integrity Guardrails


def validate_data(df):
    """Ensures data schema and sanity before visualization."""
    required_columns = {'job_title', 'salary_eur', 'country'}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Schema Mismatch! Missing: {required_columns - set(df.columns)}")

    if (df['salary_eur'] < 0).any():
        raise ValueError(
            "Data Integrity Error: Negative salary values detected.")

    return True


# Main Execution Flow
try:
    df = load_and_verify_data(DATA_URL)
    validate_data(df)

    # Sidebar Filters
    st.sidebar.header("Filters")
    countries = st.sidebar.multiselect(
        "Select Countries",
        options=df['country'].unique(),
        default=df['country'].unique()
    )

    filtered_df = df[df['country'].isin(countries)]

    # Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Jobs Monitored", len(filtered_df))
    col2.metric("Average Salary", f"€{filtered_df['salary_eur'].mean():,.0f}")

    # Visuals
    st.subheader("Salary Distribution by Job Title")
    fig = px.bar(filtered_df, x='job_title', y='salary_eur',
                 color='country', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # Raw Data Table
    st.subheader("Raw Data")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"System Operational Error: {e}")
    st.stop()
