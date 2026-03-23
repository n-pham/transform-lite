/* @bruin
name: test_transform_customers
type: duckdb.sql
tags:
  - test
description: "Unit test for transform_customers logic using mock data and shared logic"
materialization:
  type: view
custom_checks:
  - name: verify_transformation
    description: "Verify that TRIM and NULL filters work correctly on mock data"
    query: "SELECT COUNT(*) FROM test_transform_customers WHERE (customer_id = 1 AND first_name = 'John' AND last_name = 'Doe') OR (customer_id = 2 AND first_name = 'Jane' AND last_name = 'Smith')"
    value: 2
@bruin */

WITH raw_customers_mock AS (
    SELECT 1 as id, '  John ' as first_name, ' Doe  ' as last_name
    UNION ALL
    SELECT 2 as id, 'Jane' as first_name, 'Smith' as last_name
    UNION ALL
    SELECT 3 as id, NULL as first_name, 'Missing' as last_name
)

{% set source_table = 'raw_customers_mock' %}
{% include 'assets/_transform_customers_logic.sql' %}
