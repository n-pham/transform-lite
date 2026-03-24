from sqlmesh import ExecutionContext, model
from pathlib import Path
import csv

@model(
    "sqlmesh_comparison.raw_customers",
    kind="FULL",
    columns={
        "id": "integer",
        "first_name": "string",
        "last_name": "string",
    },
    description="Load raw customers from CSV into SQLMesh",
)
def execute(
    context: ExecutionContext,
    **kwargs,
) -> None:
    # Path relative to the project root
    csv_path = Path("data/raw_customers.csv")
    
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = [
            {
                "id": int(row["id"]),
                "first_name": row["first_name"],
                "last_name": row["last_name"],
            }
            for row in reader
        ]
        
        # Insert data into the model's table
        # SQLMesh will handle the table creation based on the columns defined above
        context.table("sqlmesh_comparison.raw_customers").insert(rows)
