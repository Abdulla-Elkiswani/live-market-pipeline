import csv
import os
from src.security import DataMasker
from src.database import DatabaseManager


class DataGatewayPipeline:
    """
    The main orchestrator class that reads raw data, handles structural anomalies,
    applies PII masking rules, and dispatches data to the storage layer.
    """

    def __init__(self, raw_data_path: str = "data/raw/mock_market_data.csv"):
        self.raw_data_path = raw_data_path
        self.db_manager = DatabaseManager()

    def run(self):
        """
        Executes the end-to-end ETL (Extract, Transform, Load) pipeline.
        Includes robust try-except error catching to guarantee pipeline resilience.
        """
        print("🚀 Starting Data Gateway Pipeline...")

        if not os.path.exists(self.raw_data_path):
            print(f"❌ Error: Raw data file not found at {self.raw_data_path}")
            return

        # Ensure the database table schema is initialized
        self.db_manager.initialize_schema()

        valid_records = []
        skipped_rows_count = 0

        # Open and read the raw CSV file
        with open(self.raw_data_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    row_id = int(row['row_id'])
                    job_title = row['job_title'].strip()
                    candidate_name = row['candidate_name'].strip()
                    candidate_email = row['candidate_email'].strip()
                    country = row['country'].strip()

                    # --- VALIDATION GATE 1: Check for Missing Email ---
                    if not candidate_email:
                        raise ValueError(
                            f"Missing candidate email at Row ID {row_id}")

                    # --- VALIDATION GATE 2: Check for Malformed Email ---
                    if "@" not in candidate_email:
                        raise ValueError(
                            f"Malformed email formatting ('{candidate_email}') at Row ID {row_id}")

                    # --- VALIDATION GATE 3: Type Safety on Salary ---
                    try:
                        salary_eur = int(row['salary_eur'])
                    except ValueError:
                        raise TypeError(
                            f"Invalid non-integer salary metric ('{row['salary_eur']}') at Row ID {row_id}")

                    # --- TRANSFORMATION LAYER: Apply PII Masking & Hashing ---
                    masked_name = DataMasker.obfuscate_name(candidate_name)
                    hashed_email = DataMasker.hash_email(candidate_email)

                    # Append clean data as a tuple matching our relational schema
                    valid_records.append((
                        row_id,
                        job_title,
                        masked_name,
                        hashed_email,
                        salary_eur,
                        country
                    ))

                except (ValueError, TypeError) as error:
                    # Log data anomalies clearly without crashing the entire script
                    print(f"⚠️ Row Skipped due to Data Anomaly -> {error}")
                    skipped_rows_count += 1
                    continue

        # Bulk load all the successfully transformed records into DuckDB
        if valid_records:
            self.db_manager.insert_records(valid_records)
            print(
                f"\n✅ Pipeline Complete! Successfully loaded {len(valid_records)} records into DuckDB.")

        if skipped_rows_count > 0:
            print(
                f"🛡️ Gracefully caught and isolated {skipped_rows_count} anomalous data entries.")

        self.db_manager.close()


if __name__ == "__main__":
    # This allows us to run the pipeline file directly from the terminal
    pipeline = DataGatewayPipeline()
    pipeline.run()
