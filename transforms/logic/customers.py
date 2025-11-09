from typing import Dict

def transform_raw_customer(raw_customer: Dict) -> Dict:
    """Pure function - easily testable"""
    return {
        'customer_id': raw_customer['id'],
        'first_name': raw_customer['first_name'].strip(),
        'last_name': raw_customer['last_name'].strip(),
    }