import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(page_title="Market Data Gateway", layout="wide")
st.title("Market Data Gateway: Production Monitor")

# Load data
df = duckdb.connect().execute("SELECT * FROM 'data/market_data.parquet'").df()

# Sidebar: Filters
st.sidebar.header("Filters")
countries = st.sidebar.multiselect(
    "Select Countries", options=df['country'].unique(), default=df['country'].unique())

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
