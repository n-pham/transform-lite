"""@bruin
name: raw_customers
type: python
description: "Load raw customers from CSV into DuckDB using dlt"
columns:
  - name: id
    type: integer
    description: "Primary key for customer"
    checks:
      - name: unique
      - name: not_null
  - name: first_name
    type: string
    description: "Customer's first name"
  - name: last_name
    type: string
    description: "Customer's last name"
@bruin"""
import dlt
import csv
from pathlib import Path

def run():
    # Path relative to the project root
    csv_path = Path('data/raw_customers.csv')
    
    pipeline = dlt.pipeline(
        pipeline_name="jaffle_shop",
        destination="duckdb",
        dataset_name="main"
    )

    @dlt.resource(
        write_disposition="replace",
        table_name="raw_customers"
    )
    def customers():
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield {
                    'id': int(row['id']),
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                }

    info = pipeline.run(customers())
    print(f"✓ Loaded customers: {info}")

if __name__ == "__main__":
    run()
