import os
import ibis
from typing import Any

def get_engine_session() -> ibis.BaseBackend:
    """
    Abstracts away the underlying compute hardware and manages infrastructure initializations.
    Returns a DuckDB backend for local development and a PySpark backend for production.
    """
    env = os.getenv("ENV", "local")
    
    if env == "production":
        # In a production environment, we use PySpark
        try:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.appName("IbisProduction").getOrCreate()
            return ibis.pyspark.connect(spark)
        except ImportError:
            # Fallback or error if pyspark is not available in prod
            raise ImportError("PySpark is required for production environment but not found.")
    else:
        # Local development uses DuckDB
        # We can use an in-memory or file-based DuckDB
        return ibis.duckdb.connect("jaffle_shop.duckdb")
