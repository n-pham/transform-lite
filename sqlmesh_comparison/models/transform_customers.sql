MODEL (
  name sqlmesh_comparison.transform_customers,
  kind FULL,
  description "Transform raw customers into staging customers",
  cron '@daily',
  columns (
    customer_id INTEGER,
    first_name STRING,
    last_name STRING
  )
);

SELECT
  id AS customer_id,
  TRIM(first_name) AS first_name,
  TRIM(last_name) AS last_name
FROM sqlmesh_comparison.raw_customers
WHERE
  first_name IS NOT NULL AND last_name IS NOT NULL;
