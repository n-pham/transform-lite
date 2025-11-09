export PYTHONPATH := "."

# Raw to staging layer
staging_customers: load_raw
    uv run python scripts/transform_customers.py

# Load raw data tasks
load_raw:
    uv run python scripts/load_raw_data.py