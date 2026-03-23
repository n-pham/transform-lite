SELECT
    id as customer_id,
    TRIM(first_name) as first_name,
    TRIM(last_name) as last_name
FROM {{ source_table }}
WHERE first_name IS NOT NULL 
  AND last_name IS NOT NULL
