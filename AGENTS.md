# Bruin Data Assistant

I am a helpful coding assistant with expertise in **data-Bruin** and **dlt**. This project demonstrates how to use Bruin to manage data transformations with minimal boilerplate while maintaining high standards for documentation and testing.

## Project Overview

The project utilizes Bruin to orchestrate a simple ETL pipeline:
1.  **`assets/load_customers.py`**: Uses `dlt` to ingest raw CSV data into DuckDB.
2.  **`assets/transform_customers.sql`**: A SQL asset that transforms raw data into a staging table, including metadata, documentation, and data quality tests in a single file.

## Setup Instructions

### 1. Install Bruin CLI
To install the Bruin CLI on macOS/Linux/Windows (Git Bash), run:
```bash
curl -LsSf https://getbruin.com/install/cli | sh
```
The binary is typically installed to `~/.local/bin/bruin`.

### 2. Configure Connections
The project uses `.bruin.yml` to define the DuckDB connection:
```yaml
environments:
  default:
    connections:
      duckdb:
        - name: "duckdb-default"
          path: "jaffle_shop.duckdb"
```

### 3. Initialize/Validate
To ensure the pipeline is correctly configured:
```bash
bruin validate .
```

## Core Bruin Commands

### Lineage
Visualize the upstream and downstream dependencies of an asset:
```bash
bruin lineage assets/transform_customers.sql
```

### Run Pipeline
Run all assets in the `assets/` directory (this will automatically handle dependencies and quality checks):
```bash
bruin run assets/
```

### Run with Verbose Output
To see the actual SQL queries being executed and the results of individual quality checks:
```bash
bruin run --verbose assets/transform_customers.sql
```

## Why Bruin?
*   **Single File Definition**: SQL, metadata, materialization, and tests coexist in one file (`.sql`).
*   **Built-in Data Quality**: Column-level checks like `unique`, `not_null`, and `positive` are declared directly in the asset header.
*   **Automatic Materialization**: Bruin handles `CREATE TABLE AS` or `INSERT INTO` logic based on the `materialization` metadata.
*   **Python Integration**: Seamlessly mix Python assets (using `dlt` or pure Python) with SQL transformations.
