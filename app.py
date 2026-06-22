import streamlit as st
import duckdb
import os
import duckdb
# DuckDB can query Parquet files directly without a database file
conn = duckdb.connect()
df = conn.execute("SELECT * FROM 'market_data.parquet'").df()

# 1. Page Configuration
st.set_page_config(page_title="Market Data Gateway", layout="wide")

# 2. UI Header
st.title("Market Data Gateway: Production Monitor")

# 3. Safe Database Connection
db_path = 'data/processed/market_data.duckdb'

if os.path.exists(db_path):
    try:
        conn = duckdb.connect(db_path, read_only=True)
        # Add your dashboard display code here
        st.success("Database connected successfully!")
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
else:
    st.warning(f"Database file not found at {db_path}.")
    st.info("The dashboard is currently in monitor-only mode. Please ensure the data pipeline is running.")
