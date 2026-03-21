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
custom_checks:
  - name: unit_test
    description: "Fail if mock is wrong"
    query: "SELECT COUNT(*) FROM transform_customers WHERE (customer_id = 1 AND first_name = 'John' AND last_name = 'Doe')
                                                        OR (customer_id = 2 AND first_name = 'Jane' AND last_name = 'Smith')"
    value: 2
@bruin */

-- 1. DEFINE MOCK DATA
WITH raw_customers_mock AS (
    SELECT 1 as id, '  John ' as first_name, ' Doe  ' as last_name
    UNION ALL
    SELECT 2 as id, 'Jane' as first_name, 'Smith' as last_name
),

-- 2. JINJA ENVIRONMENT SWITCH
raw_customers_source AS (
    {% if (env | default('test')) == 'test' %}
    SELECT * FROM raw_customers_mock
    {% else %}
    SELECT * FROM raw_customers
    {% endif %}
),

-- 3. FINAL TRANSFORMATION
final AS (
    SELECT
        id as customer_id,
        TRIM(first_name) as first_name,
        TRIM(last_name) as last_name
    FROM raw_customers_source
    WHERE first_name IS NOT NULL 
      AND last_name IS NOT NULL
)

SELECT * FROM final