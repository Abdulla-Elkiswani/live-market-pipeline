import duckdb
import random
import time
from datetime import datetime

DB_PATH = 'data/processed/market_data.duckdb'


def generate_random_record():
    titles = ['AI Engineer', 'Cloud Architect',
              'Data Engineer', 'Data Scientist', 'DevOps Engineer']
    countries = ['Germany', 'France', 'USA', 'UK', 'Netherlands', 'Spain']
    return {
        'job_title': random.choice(titles),
        'salary_eur': random.randint(50000, 150000),
        'country': random.choice(countries)
    }


def run_streamer():
    print("🚀 Data Streamer started. Press Ctrl+C to stop.")
    conn = duckdb.connect(DB_PATH)

    try:
        while True:
            data = generate_random_record()
            # Calculate next ID
            result = conn.execute(
                "SELECT MAX(row_id) + 1 FROM job_metrics").fetchone()[0]
            next_id = result if result is not None else 1

            # Insert with CURRENT_TIMESTAMP for the trend line
            conn.execute("""
                INSERT INTO job_metrics (row_id, job_title, salary_eur, country, created_at) 
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (next_id, data['job_title'], data['salary_eur'], data['country']))

            print(
                f"Ingested: {data['job_title']} in {data['country']} (ID: {next_id})")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nStreamer stopped.")
    finally:
        conn.close()


if __name__ == "__main__":
    run_streamer()
