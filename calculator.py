# calculator.py
import math
from typing import List, Dict, Any


def calculate_truck_breakdown(total_yards: float, yard_capacity: float = 10.0) -> Dict[str, Any]:
    """
    Calculates total trucks needed and breaks down full loads vs. partial/remainder load.
    Example: 24 CY @ 10 CY/truck -> 3 trucks total (2 full @ 10 CY + 1 partial @ 4 CY).
    """
    if total_yards <= 0 or yard_capacity <= 0:
        return {
            "total_trucks": 0,
            "full_trucks": 0,
            "remainder_yards": 0.0,
            "breakdown_text": "0 trucks (0.0 CY)",
        }

    total_trucks = math.ceil(total_yards / yard_capacity)
    remainder = round(total_yards % yard_capacity, 2)

    if remainder == 0:
        full_trucks = total_trucks
        breakdown_text = f"{total_trucks} full truck(s) @ {yard_capacity:.1f} CY"
    else:
        full_trucks = total_trucks - 1
        if full_trucks > 0:
            breakdown_text = f"{full_trucks} full ({yard_capacity:.1f} CY) + 1 partial ({remainder:.1f} CY)"
        else:
            breakdown_text = f"1 partial load ({remainder:.1f} CY)"

    return {
        "total_trucks": total_trucks,
        "full_trucks": full_trucks,
        "remainder_yards": remainder,
        "breakdown_text": breakdown_text,
    }


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