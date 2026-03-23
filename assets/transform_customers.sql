/* @bruin
name: transform_customers
type: duckdb.sql
description: "Transform raw customers into staging customers with data quality checks"
depends:
  - raw_customers
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

{% set source_table = 'raw_customers' %}
{% include 'assets/_transform_customers_logic.sql' %}