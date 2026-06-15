from sqlmesh import model
import pandas as pd
from sqlmesh_duckdb_spark.utils import spark_model

@model(
    "sqlmesh_duckdb_spark.raw_customers",
    kind="FULL",
    columns={
        "id": "integer",
        "first_name": "string",
        "last_name": "string",
    },
)
@spark_model
def execute(context, spark, F, **kwargs):
    # Logic remains simple, branching is hidden in decorator
    df = pd.read_csv("data/raw_customers.csv")
    
    # We return the dataframe; the decorator handles converting to Spark if in Prod
    # or keeping as Pandas if Local.
    return df
