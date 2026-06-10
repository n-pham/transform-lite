from ibis.expr.types import Table

def transform_customers(customers: Table) -> Table:
    """
    Pure transformation logic - the "source of truth" for analytics engineering rules.
    This function has zero knowledge of the underlying infrastructure.
    
    Args:
        customers: An Ibis table expression containing raw customer data.
        
    Returns:
        A transformed Ibis table expression.
    """
    return customers.mutate(
        customer_id=customers.id,
        first_name=customers.first_name.strip(),
        last_name=customers.last_name.strip(),
    ).select(
        "customer_id", 
        "first_name", 
        "last_name"
    )
