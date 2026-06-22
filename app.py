import streamlit as st
import pandas as pd
import requests
import io


DATA_URL = "https://github.com/Abdulla-Elkiswani/live-market-pipeline/releases/download/v1.0.0/market_data.parquet"


@st.cache_data(ttl=600)
def load_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Good practice to check if the download worked
    return pd.read_parquet(io.BytesIO(response.content))


# Load data with error handling
try:
    df = load_data(DATA_URL)
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()
