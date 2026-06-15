from sqlmesh import model
import pandas as pd
from sqlmesh_duckdb_spark.utils import spark_model

@model(
    "sqlmesh_duckdb_spark.transform_customers",
    columns={
        "customer_id": "int",
        "first_name": "string",
        "last_name": "string",
    },
    kind="FULL",
)
@spark_model
def execute(context, spark, F, **kwargs):
    # Fetch upstream data
    table = context.table("sqlmesh_duckdb_spark.raw_customers")
    df = context.fetchdf(f"SELECT * FROM {table}")
    
    # Convert to Spark-compatible DataFrame if needed
    spark_df = spark.createDataFrame(df) if isinstance(df, pd.DataFrame) else df

    # Pure Spark Logic (No branching!)
    return (
        spark_df
        .filter(F.col("first_name").isNotNull() & F.col("last_name").isNotNull())
        .select(
            F.col("id").alias("customer_id"),
            F.trim(F.col("first_name")).alias("first_name"),
            F.trim(F.col("last_name")).alias("last_name")
        )
    )
