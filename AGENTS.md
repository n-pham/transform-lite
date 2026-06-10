# Bruin Data Assistant

I am a helpful coding assistant with expertise in **dbt core**, **data-Bruin** and **dlt**. This project demonstrates how to manage data transformations with various technologies, with minimal boilerplate while maintaining high standards for documentation and testing.

## Project 2: Ibis & DuckDB/PySpark

This project uses `ibis` to create a portable transformation layer that runs on DuckDB for local development and PySpark for production.

### Files

#### `config.py`
This module abstracts away the underlying compute hardware and manages infrastructure initializations.
- `get_engine_session() -> ibis.BaseBackend`: Returns the appropriate Ibis backend based on the environment.

#### `transformations.py`
This module acts as the isolated "source of truth" for your analytics engineering rules. It has zero knowledge of cloud environments, cluster sizes, or infrastructure.

#### `main.py`
The master execution script and pipeline entry point. It manages data routing (I/O) and glues your environment configuration to your business logic.
- `run_pipeline() -> None`: Orchestrates the entire end-to-end lifecycle of the execution run.
  - Invokes `get_engine_session()` to securely set up the active execution layer.
  - Binds source data based on the context: reads massive, production-grade cloud tables via `con.table()` in production, or instantly streams lightweight mock test files from your computer's storage using `con.read_parquet()` during local development.

### How to Run

To run the Ibis pipeline locally:
```bash
# Set PYTHONPATH to include the root directory
export PYTHONPATH=$PYTHONPATH:.
# Run the pipeline using uv
uv run python ibis_project/main.py
```

---

## Project 1: Bruin Overview

The project utilizes Bruin to orchestrate a simple ETL pipeline:
1.  **`assets/load_customers.py`**: Uses `dlt` to ingest raw CSV data into DuckDB.
2.  **`assets/transform_customers.sql`**: A SQL asset that transforms raw data into a staging table, using shared logic from `assets/_transform_customers_logic.sql`.
3.  **`assets/test_transform_customers.sql`**: A dedicated test asset tagged with `test` that injects mock data into the shared logic.

## Mandatory Unit Test Instruction

All SQL models require unit tests written in a separate asset file (e.g., `assets/test_model_name.sql`). To avoid duplicating logic, the core transformation SQL must be moved to a shared partial file (e.g., `assets/_model_logic.sql`) and included in both the production and test assets using Jinja `{% include %}`.

The test asset must:
1.  Be tagged with `test`.
2.  Inject mock data into the shared logic.
3.  Include a `custom_check` to verify the output against expected values.

To run the pipeline:
- **Production Run**: `bruin run --exclude-tag test`
- **Unit Test Run**: `bruin run --tag test`

See `assets/transform_customers.sql` and `assets/test_transform_customers.sql` for an example of this pattern.

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
