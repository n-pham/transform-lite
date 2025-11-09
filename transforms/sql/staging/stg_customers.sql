SELECT
    id as customer_id,
    {{ trim('first_name') }} as first_name,
    {{ trim('last_name') }} as last_name

FROM {{ source('jaffle_shop', 'customers') }}

WHERE first_name IS NOT NULL
  AND last_name IS NOT NULL
