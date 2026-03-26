"""
Budget calculation utilities for inflation adjustments.
"""

import math
from datetime import datetime, timedelta


def calculate_adjusted_budget(original_budget: float, inflation_rate: float, months: int = 1) -> float:
    """
    Calculate budget adjustment based on inflation.
    
    Args:
        original_budget: The base budget amount
        inflation_rate: Annual inflation rate as percentage
        months: Number of months to project (default: 1)
    
    Returns:
        Adjusted budget amount accounting for inflation
    """
    monthly_rate = inflation_rate / 12 / 100
    return original_budget * math.pow(1 + monthly_rate, months)


def calculate_purchasing_power_loss(inflation_rate: float, months: int = 12) -> float:
    """
    Calculate cumulative purchasing power loss over time.
    
    Args:
        inflation_rate: Annual inflation rate as percentage
        months: Time period in months
    
    Returns:
        Percentage of purchasing power lost
    """
    monthly_rate = inflation_rate / 12 / 100
    loss = (1 - math.pow(1 / (1 + monthly_rate), months)) * 100
    return round(loss, 2)


def category_adjustment(base_amount: float, inflation_rate: float, category_multiplier: float = 1.0) -> float:
    """
    Calculate adjusted amount for a specific category with optional multiplier.
    
    Args:
        base_amount: Base budget for the category
        inflation_rate: Annual inflation rate
        category_multiplier: Category-specific inflation multiplier (1.0 = baseline)
    
    Returns:
        Adjusted budget for the category
    """
    adjusted_rate = inflation_rate * category_multiplier
    return calculate_adjusted_budget(base_amount, adjusted_rate)


def get_category_inflation_multipliers() -> dict:
    """
    Get inflation sensitivity multipliers for different categories.
    Categories more affected by inflation have higher multipliers.
    
    Returns:
        Dictionary of category multipliers
    """
    return {
        "Housing": 1.2,           # Often more sensitive to inflation
        "Food & Groceries": 1.5,  # Volatile commodity prices
        "Transportation": 1.3,    # Fuel prices vary significantly
        "Utilities": 1.4,         # Energy prices affect heavily
        "Healthcare": 1.6,        # Rising healthcare costs
        "Insurance": 1.1,         # Moderate inflation impact
        "Entertainment": 0.8,     # Often less affected
        "Dining Out": 1.2,        # Food service inflation
        "Shopping": 0.9,          # Varies by retail sector
        "Subscriptions": 0.7,     # Often stable pricing
        "Education": 1.3,         # Tuition rises faster than inflation
        "Other": 1.0              # Baseline
    }


def breakdown_adjusted_budget(budget_breakdown: dict, inflation_rate: float) -> dict:
    """
    Calculate adjusted amounts for multiple categories.
    
    Args:
        budget_breakdown: Dictionary of {category: amount}
        inflation_rate: Annual inflation rate
    
    Returns:
        Dictionary with adjusted amounts and deltas
    """
    multipliers = get_category_inflation_multipliers()
    adjusted = {}
    
    for category, amount in budget_breakdown.items():
        multiplier = multipliers.get(category, 1.0)
        adjusted_amount = category_adjustment(amount, inflation_rate, multiplier)
        
        adjusted[category] = {
            "original": amount,
            "adjusted": adjusted_amount,
            "delta": adjusted_amount - amount,
            "percent_change": ((adjusted_amount - amount) / amount * 100) if amount > 0 else 0,
            "multiplier": multiplier
        }
    
    return adjusted
