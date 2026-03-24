MODEL (
  name sqlmesh_comparison.stg_customers,
  kind FULL,
  description "Staging customers from jaffle_shop",
);

SELECT
  id AS customer_id,
  {{ trim('first_name') }} AS first_name,
  {{ trim('last_name') }} AS last_name
FROM jaffle_shop.customers
WHERE
  first_name IS NOT NULL AND last_name IS NOT NULL;
