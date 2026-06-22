# Live Market Pipeline

A decoupled, real-time data ingestion and analytics platform built for high-concurrency monitoring.

## Overview
This project demonstrates a robust data pipeline architecture that separates data production (ingestion) from data consumption (visualization). It is designed to handle simultaneous read/write operations without locking, utilizing the SWMR (Single-Writer, Multi-Reader) model.

## Tech Stack
- **Ingestion Engine:** Python-based streaming process.
- **Database:** DuckDB (Atomic, high-performance analytical storage).
- **Visualization:** Streamlit (Reactive, real-time dashboard).
- **Architecture:** Decoupled concurrency via SWMR (Single-Writer, Multi-Reader) patterns.

## Key Engineering Concepts
- **Concurrency:** Managed via DuckDB's SWMR architecture to ensure stable performance under load.
- **Data Integrity:** ACID-compliant transactions (Atomic/Consistent) ensuring data is never corrupted during ingestion.
- **Latency Management:** TTL-based caching strategies to balance dashboard performance and data freshness.

## Dashboard Features
- **Real-Time Visualization:** Interactive bar charts and automated data updates.
- **Trend Analysis:** Time-series tracking of key metrics using `created_at` timestamps.
- **Dynamic Filtering:** User-driven analytics for multi-dimensional data exploration across different regions.

## How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/abdulla-elkiswani/live-market-pipeline.git](https://github.com/abdulla-elkiswani/live-market-pipeline.git)
   cd live-market-pipeline
