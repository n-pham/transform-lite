/* @bruin
name: transform_customers
type: duckdb.sql
description: "Transform raw customers into staging customers with data quality checks"
depends:
  - load_customers
materialization:
  type: table
columns:
  - name: customer_id
    type: integer
    description: "Unique identifier for customer"
    checks:
      - name: unique
      - name: not_null
      - name: positive
  - name: first_name
    type: string
    description: "Cleaned first name"
    checks:
      - name: not_null
  - name: last_name
    type: string
    description: "Cleaned last name"
    checks:
      - name: not_null
@bruin */

SELECT
    id as customer_id,
    TRIM(first_name) as first_name,
    TRIM(last_name) as last_name
FROM raw_customers
WHERE first_name IS NOT NULL
  AND last_name IS NOT NULL
