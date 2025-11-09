from transforms.logic.customers import transform_raw_customer

def test_transform_raw_customer():
    raw = {'id': 1, 'first_name': 'John', 'last_name': 'Doe'}
    result = transform_raw_customer(raw)
    assert result['customer_id'] == 1