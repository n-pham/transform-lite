from functools import wraps
import pandas as pd

def spark_model(func):
    """
    A decorator to encapsulate DuckDB/Spark branching.
    - Provides a 'spark' session and 'F' (functions) to the model.
    - Handles return type branching (Pandas for local, Spark DF for prod).
    """
    @wraps(func)
    def wrapper(context, **kwargs):
        # 1. Determine Engine
        if context.gateway == "local":
            from duckdb.experimental.spark.sql import SparkSession
            from duckdb.experimental.spark.sql import functions as F
        else:
            from pyspark.sql import SparkSession
            from pyspark.sql import functions as F
        
        spark = SparkSession.builder.getOrCreate()
        
        # 2. Execute the user logic
        # We pass spark and F into the function so the user doesn't import them
        result = func(context, spark, F, **kwargs)
        
        # 3. Handle Return Branching
        if context.gateway == "local":
            # If it's already a pandas DF (like in raw_customers), return it
            if isinstance(result, pd.DataFrame):
                return result
            # Otherwise convert Spark-style DF to Pandas
            return result.toPandas()
        
        return result
    
    return wrapper
