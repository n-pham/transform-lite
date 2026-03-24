-- SQLMesh macros are defined as Jinja functions
{% macro trim(column_name) %}
  TRIM({{ column_name }})
{% endmacro %}
