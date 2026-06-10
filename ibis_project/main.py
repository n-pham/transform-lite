import os
import ibis
from ibis.expr.types import Table
from ibis_project.config import get_engine_session
from ibis_project.transformations import transform_customers

def run_pipeline() -> None:
    """
    Orchestrates the entire end-to-end lifecycle of the execution run.
    """
    # 1. Securely set up the active execution layer
    con: ibis.BaseBackend = get_engine_session()
    
    env: str = os.getenv("ENV", "local")
    
    # 2. Bind source data based on the context
    customers: Table
    if env == "production":
        # Reads massive, production-grade cloud tables
        customers = con.table("raw_customers")
    else:
        # Instantly streams lightweight mock test files from local storage
        # Assuming a parquet file exists for local development/testing
        data_path: str = "data/raw_customers.parquet"
        
        # If the parquet doesn't exist, we might want to check for CSV or create it
        if not os.path.exists(data_path):
            # Fallback to CSV if parquet is missing for this demo
            customers = con.read_csv("data/raw_customers.csv")
        else:
            customers = con.read_parquet(data_path)
    
    # 3. Apply business logic
    transformed: Table = transform_customers(customers)
    
    # 4. Routing output (In a real app, this would be con.to_parquet or con.insert)
    print("Execution complete. Preview of transformed data:")
    # We only call .execute() at the very end to trigger computation
    print(transformed.limit(5).execute())

if __name__ == "__main__":
    run_pipeline()
