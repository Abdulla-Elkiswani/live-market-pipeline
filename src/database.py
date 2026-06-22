import duckdb


class DatabaseManager:
    """
    Manages the lifecycle of the local DuckDB database instance,
    including connection handling, schema creation, and data insertion.
    """

    def __init__(self, db_path: str = "data/processed/market_data.duckdb"):
        """
        Initializes the database manager with a path to the database file.
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establishes a connection to the local DuckDB database file."""
        if not self.conn:
            self.conn = duckdb.connect(self.db_path)

    def close(self):
        """Safely closes the database connection if it exists."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_schema(self):
        """
        Creates the target analytical table if it doesn't already exist.
        Defines strict relational data types for type integrity.
        """
        self.connect()

        # We define a strict schema. Notice that we don't store plain names or emails.
        # We store the masked name, the hashed email fingerprint, and verified metrics.
        create_table_query = """
        CREATE TABLE IF NOT EXISTS job_metrics (
            row_id INTEGER PRIMARY KEY,
            job_title VARCHAR,
            masked_name VARCHAR,
            hashed_email VARCHAR,
            salary_eur INTEGER,
            country VARCHAR
        );
        """
        self.conn.execute(create_table_query)

    def insert_records(self, records: list[tuple]):
        """
        Inserts multiple validated and masked records into the database in bulk.
        Expects a list of tuples matching the database table schema.
        """
        self.connect()
        if not records:
            return

        # DuckDB handles standard parameterized SQL text queries efficiently
        insert_query = """
        INSERT INTO job_metrics (row_id, job_title, masked_name, hashed_email, salary_eur, country)
        VALUES (?, ?, ?, ?, ?, ?);
        """

        # executemany runs bulk insertions safely and prevents SQL injection vulnerabilities
        self.conn.executemany(insert_query, records)
