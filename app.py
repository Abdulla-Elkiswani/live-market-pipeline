import streamlit as st
import duckdb
import os

# 1. Page Configuration
st.set_page_config(page_title="Market Data Gateway", layout="wide")

# 2. UI Header
st.title("Market Data Gateway: Production Monitor")

# 3. Path to the Parquet data file
data_path = 'data/market_data.parquet'

# 4. Data Loading Logic


def load_data(path):
    if not os.path.exists(path):
        return None
    try:
        # DuckDB can query Parquet files directly
        conn = duckdb.connect()
        df = conn.execute(f"SELECT * FROM '{path}'").df()
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# 5. Display the data
df = load_data(data_path)

if df is not None:
    st.success("Data loaded successfully!")
    st.dataframe(df, use_container_width=True)
else:
    st.warning(
        "Data file not found. Ensure 'data/market_data.parquet' is in the repository.")
    st.info(
        "If you just pushed your changes, wait a moment for the redeployment to finish.")

#
