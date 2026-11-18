# calculator.py
import math
from typing import List, Dict


def estimate_trucks(total_yards: float, yard_capacity: float = 10.0) -> int:
    """Calculates required concrete mixer trucks based on max yard capacity per load."""
    if total_yards <= 0 or yard_capacity <= 0:
        return 0
    return math.ceil(total_yards / yard_capacity)


def calculate_quote_totals(line_items: List[Dict], tax_rate: float) -> Dict[str, float]:
    """Computes subtotal, sales tax, and grand total from active line items."""
    sub_total = sum(item["Amount"] for item in line_items)
    tax_amount = sub_total * tax_rate
    grand_total = sub_total + tax_amount
    return {
        "sub_total": sub_total,
        "tax_amount": tax_amount,
        "grand_total": grand_total,
    }