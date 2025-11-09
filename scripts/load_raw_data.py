"""
Load raw CSV data into DuckDB
"""
import dlt
import csv
from pathlib import Path

@dlt.resource(
    write_disposition="replace",
    table_name="raw_jaffle_shop_customers"
)
def load_customers():
    """Load raw customers from CSV"""
    csv_path = Path(__file__).parent.parent / 'data' / 'raw_customers.csv'
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                'id': int(row['id']),
                'first_name': row['first_name'],
                'last_name': row['last_name'],
            }

@dlt.resource(
    write_disposition="replace",
    table_name="raw_jaffle_shop_orders"
)
def load_orders():
    """Load raw orders from CSV"""
    csv_path = Path(__file__).parent.parent / 'data' / 'raw_orders.csv'
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                'id': int(row['id']),
                'user_id': int(row['user_id']),
                'order_date': row['order_date'],
                'status': row['status'],
            }

@dlt.resource(
    write_disposition="replace",
    table_name="raw_jaffle_shop_payments"
)
def load_payments():
    """Load raw payments from CSV"""
    csv_path = Path(__file__).parent.parent / 'data' / 'raw_payments.csv'
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                'id': int(row['id']),
                'order_id': int(row['order_id']),
                'payment_method': row['payment_method'],
                'amount': float(row['amount']) / 100,  # Convert cents to dollars
                'status': row['status'],
            }

def main():
    """Load all raw data"""
    pipeline = dlt.pipeline(
        pipeline_name="jaffle_shop",
        destination="duckdb",
        dataset_name="main",
        dev_mode=False
    )
    
    # Load all raw tables
    load_info = pipeline.run([
        load_customers(),
        # load_orders(),
        # load_payments(),
    ])
    
    print(f"✓ Raw data loaded: {load_info}")
    
    # Verify counts
    with pipeline.sql_client() as client:
        for table in [
            'raw_jaffle_shop_customers',
            # 'raw_jaffle_shop_orders',
            # 'raw_jaffle_shop_payments'
        ]:
            result = client.execute_sql(f"SELECT COUNT(*) FROM main.{table}")
            count = result[0][0]
            print(f"  {table}: {count} rows")

if __name__ == "__main__":
    main()
