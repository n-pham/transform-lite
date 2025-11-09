"""
This script runs the dlt pipeline to transform customer data.
"""
import dlt
from transforms.resources.staging_customers import staging_customers_sql

# Run the pipeline
pipeline = dlt.pipeline(
    pipeline_name="jaffle_shop",
    destination="duckdb",
    dataset_name="main",
    dev_mode=False
)

# Use SQL-based transformation
load_info = pipeline.run(staging_customers_sql(pipeline))
print(f"✓ Loaded {load_info}")

# Verify results
with pipeline.sql_client() as client:
    result = client.execute_sql("SELECT COUNT(*) FROM main.stg_customers")
    count = result[0][0]
    print(f"✓ Staging customers count: {count}")
