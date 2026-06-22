import streamlit as st
import duckdb
import time

st.set_page_config(page_title="Raisin Engineering Dashboard", layout="wide")

# --- UI Header ---
st.title("🚀 Raisin Data Gateway: Production Monitor")

# --- Live Mode Logic ---
if st.sidebar.checkbox("Enable Live Mode (Auto-Refresh)"):
    time.sleep(3)
    st.rerun()

# --- Sidebar Filters ---
st.sidebar.header("Analytics Filters")
conn = duckdb.connect('data/processed/market_data.duckdb', read_only=True)
all_countries = conn.execute(
    "SELECT DISTINCT country FROM job_metrics WHERE country IS NOT NULL").df()['country'].tolist()
conn.close()

selected_country = st.sidebar.multiselect(
    "Select Country", options=all_countries, key="country_filter")

# --- Data Fetching ---


def get_data(countries):
    conn = duckdb.connect('data/processed/market_data.duckdb', read_only=True)
    query = "SELECT job_title, avg(salary_eur) as avg_salary FROM job_metrics"
    if countries:
        country_list = ", ".join([f"'{c}'" for c in countries])
        query += f" WHERE country IN ({country_list})"
    query += " GROUP BY job_title ORDER BY avg_salary DESC"
    df = conn.execute(query).df()
    conn.close()
    return df


# --- Metrics Section ---
conn = duckdb.connect('data/processed/market_data.duckdb', read_only=True)
total_records = conn.execute("SELECT count(*) FROM job_metrics").fetchone()[0]
avg_sal = conn.execute("SELECT avg(salary_eur) FROM job_metrics").fetchone()[0]
conn.close()

col1, col2 = st.columns(2)
col1.metric("Total Records Ingested", total_records)
col2.metric("Market Average Salary (EUR)", f"{avg_sal:,.0f}" if avg_sal else 0)

# --- Charts ---
tab1, tab2 = st.tabs(["Salary Distribution", "Salary Trend"])

with tab1:
    st.subheader("Average Salaries by Job Title")
    df = get_data(selected_country)
    if not df.empty:
        st.bar_chart(df.set_index('job_title'))
    else:
        st.info("No data available.")

with tab2:
    st.subheader("Market Salary Trend")
    conn = duckdb.connect('data/processed/market_data.duckdb', read_only=True)
    trend_df = conn.execute(
        "SELECT created_at, avg(salary_eur) as avg_sal FROM job_metrics GROUP BY created_at ORDER BY created_at").df()
    conn.close()
    if not trend_df.empty:
        st.line_chart(trend_df.set_index('created_at'))
    else:
        st.write("Waiting for more data to generate trend...")
