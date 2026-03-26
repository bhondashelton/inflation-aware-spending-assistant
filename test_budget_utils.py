"""
Tests for budget calculation utilities.
"""

import unittest
from budget_utils import (
    calculate_adjusted_budget,
    calculate_purchasing_power_loss,
    category_adjustment,
    breakdown_adjusted_budget
)


class TestBudgetCalculations(unittest.TestCase):
    """Test suite for budget utility functions."""
    
    def test_calculate_adjusted_budget_basic(self):
        """Test basic budget adjustment calculation."""
        original = 1000
        inflation_rate = 3.0
        
        adjusted = calculate_adjusted_budget(original, inflation_rate, months=12)
        
        # Should be approximately 1030 (3% increase)
        self.assertAlmostEqual(adjusted, 1030, delta=5)
    
    def test_calculate_adjusted_budget_zero_inflation(self):
        """Test that zero inflation produces no change."""
        original = 1000
        adjusted = calculate_adjusted_budget(original, 0, months=12)
        self.assertEqual(adjusted, original)
    
    def test_calculate_adjusted_budget_monthly(self):
        """Test monthly budget adjustments."""
        original = 1000
        inflation_rate = 3.0
        
        adjusted = calculate_adjusted_budget(original, inflation_rate, months=1)
        
        # Should be approximately 1025 (0.25% for one month)
        self.assertGreater(adjusted, original)
        self.assertLess(adjusted, original * 1.01)
    
    def test_purchasing_power_loss(self):
        """Test purchasing power loss calculation."""
        inflation_rate = 3.0
        loss = calculate_purchasing_power_loss(inflation_rate, months=12)
        
        # Should be approximately 3% loss
        self.assertAlmostEqual(loss, 3.0, delta=0.5)
    
    def test_category_adjustment_multiplier(self):
        """Test category adjustment with multiplier."""
        base = 1000
        inflation_rate = 3.0
        
        # Category with 1.5x multiplier should have larger adjustment
        adjusted = category_adjustment(base, inflation_rate, category_multiplier=1.5)
        normal = calculate_adjusted_budget(base, inflation_rate)
        
        self.assertGreater(adjusted, normal)
    
    def test_breakdown_adjusted_budget(self):
        """Test breakdown of multiple categories."""
        breakdown = {
            "Housing": 1000,
            "Food & Groceries": 500,
            "Transportation": 300
        }
        inflation_rate = 3.0
        
        adjusted = breakdown_adjusted_budget(breakdown, inflation_rate)
        
        # Check structure
        self.assertEqual(len(adjusted), 3)
        for category in breakdown:
            self.assertIn(category, adjusted)
            self.assertIn("original", adjusted[category])
            self.assertIn("adjusted", adjusted[category])
            self.assertIn("delta", adjusted[category])
    
    def test_breakdown_adjustments_are_positive(self):
        """Test that positive inflation produces positive adjustments."""
        breakdown = {
            "Housing": 1000,
            "Food & Groceries": 500
        }
        
        adjusted = breakdown_adjusted_budget(breakdown, inflation_rate=3.0)
        
        for category, values in adjusted.items():
            self.assertGreater(values["adjusted"], values["original"])
            self.assertGreater(values["delta"], 0)


if __name__ == "__main__":
    unittest.main()
