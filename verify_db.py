import duckdb

print("📊 Connecting to processed DuckDB storage...")
# Connect to the local database file in read-only mode to inspect it
conn = duckdb.connect("data/processed/market_data.duckdb", read_only=True)

# Run a standard SQL query to grab the top 5 records
print("\n=== SAMPLE RECORDS FROM JOB_METRICS ===")
query = "SELECT row_id, job_title, masked_name, hashed_email, salary_eur, country FROM job_metrics LIMIT 5;"
result = conn.execute(query).fetchall()

# Print out the records neatly line by line
for row in result:
    print(row)

# Run an aggregate calculation to see total records and average salary
print("\n=== PIPELINE METRICS SUMMARY ===")
summary_query = "SELECT COUNT(*), ROUND(AVG(salary_eur), 2) FROM job_metrics;"
count, avg_salary = conn.execute(summary_query).fetchone()
print(f"Total Successful Records in DB: {count}")
print(f"Average Clean Salary: €{avg_salary}")

conn.close()
