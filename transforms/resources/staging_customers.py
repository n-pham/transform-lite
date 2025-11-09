"""
Staging: Customers
"""
import dlt
from transforms.sql_macros import render_sql, get_sql_path
from transforms.logic.customers import transform_raw_customer

@dlt.resource(
    write_disposition="replace",
    table_name="stg_customers"
)
def staging_customers_sql(pipeline: dlt.Pipeline):
    """
    Load customers using SQL transformation
    """
    # Render SQL template
    query = render_sql(get_sql_path('staging', 'stg_customers'))
    
    # Get pipeline and execute SQL
    with pipeline.sql_client() as client:
        result = client.execute_sql(query)
        for row in result:
            yield {
                'customer_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
            }

@dlt.resource(
    write_disposition="replace",
    table_name="stg_customers"
)
def staging_customers_python(pipeline: dlt.Pipeline):
    """
    Load customers using Python transformation (for testing)
    Alternative to SQL-based transformation
    """
    # Read raw data
    with pipeline.sql_client() as client:
        result = client.execute_sql("SELECT * FROM main.raw_jaffle_shop_customers")
        raw_customers = result
    
    # Transform using pure Python logic
    for row in raw_customers:
        raw_customer = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
        }
        try:
            transformed = transform_raw_customer(raw_customer)
            yield transformed
        except ValueError as e:
            print(f"Skipping invalid customer: {e}")
            continue

