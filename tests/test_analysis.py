"""
Test Suite: Statistical Analysis & Analytical Functions (TC-T-06 to TC-T-10)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import unittest
import math
import re

class TestAnalysisFormulas(unittest.TestCase):

    def setUp(self):
        # Deterministic tiny fixture dataset (5 records) for KPI formula auditing
        self.fixture_reviews = [
            {"rating": 5, "sentiment": +0.80, "sentiment_label": "Positive", "is_verified": 1, "return_intent": 0, "text": "Outstanding product, highly recommend!"},
            {"rating": 4, "sentiment": +0.40, "sentiment_label": "Positive", "is_verified": 1, "return_intent": 0, "text": "Good quality, works fine."},
            {"rating": 3, "sentiment": +0.00, "sentiment_label": "Neutral",  "is_verified": 0, "return_intent": 0, "text": "Average item, nothing special."},
            {"rating": 1, "sentiment": -0.80, "sentiment_label": "Negative", "is_verified": 1, "return_intent": 1, "text": "Defective battery, returning it for refund."},
            {"rating": 2, "sentiment": -0.60, "sentiment_label": "Negative", "is_verified": 0, "return_intent": 1, "text": "Damaged box, replacement needed."}
        ]

    def test_tc_t_06_kpi_formulas_on_known_dataset(self):
        """TC-T-06: Verify KPI formulas against deterministic known fixture."""
        n = len(self.fixture_reviews)
        ratings = [r["rating"] for r in self.fixture_reviews]
        
        # 1. Mean Star Rating: (5 + 4 + 3 + 1 + 2) / 5 = 15 / 5 = 3.00
        mean_rating = sum(ratings) / n
        self.assertAlmostEqual(mean_rating, 3.00, places=2)

        # 2. Negative Review Ratio: ratings <= 2 -> (1, 2) = 2 / 5 = 0.40 (40.0%)
        neg_count = sum(1 for r in self.fixture_reviews if r["rating"] <= 2)
        neg_ratio = neg_count / n
        self.assertAlmostEqual(neg_ratio, 0.40, places=2)

        # 3. Net Sentiment Score: Pos % (2/5=40%) - Neg % (2/5=40%) = 0.0 pts
        pos_count = sum(1 for r in self.fixture_reviews if r["sentiment_label"] == "Positive")
        neg_sent_count = sum(1 for r in self.fixture_reviews if r["sentiment_label"] == "Negative")
        nss = ((pos_count - neg_sent_count) / n) * 100.0
        self.assertAlmostEqual(nss, 0.0, places=2)

        # 4. Return Intent Rate: 2 out of 5 = 40.0%
        return_count = sum(1 for r in self.fixture_reviews if r["return_intent"] == 1)
        return_rate = (return_count / n) * 100.0
        self.assertAlmostEqual(return_rate, 40.0, places=2)

        # 5. Verified Buyer Share: 3 out of 5 = 60.0%
        verified_count = sum(1 for r in self.fixture_reviews if r["is_verified"] == 1)
        verified_share = (verified_count / n) * 100.0
        self.assertAlmostEqual(verified_share, 60.0, places=2)

    def test_tc_t_09_return_intent_regex(self):
        """TC-T-09: Verify regex classification logic for return intent detection."""
        pattern = re.compile(r'\b(return|returned|returning|refund|replace|replacement|defective|damaged)\b', re.IGNORECASE)
        
        test_sentences = [
            ("The product is completely defective and I am returning it for refund.", True),
            ("Arrived damaged in transit, requesting replacement.", True),
            ("Wonderful product, arrived safe and sound.", False),
            ("Great battery life and fast charging.", False)
        ]
        for sentence, expected_flag in test_sentences:
            match = bool(pattern.search(sentence))
            self.assertEqual(match, expected_flag, f"Regex failed on sentence: {sentence}")

    def test_tc_t_10_vendor_compliance_logic(self):
        """TC-T-10: Verify vendor SLA compliance evaluation logic."""
        def evaluate_vendor_sla(avg_rating, neg_ratio):
            if avg_rating < 4.0 or neg_ratio >= 0.10:
                return "Non-Compliant"
            return "Compliant"

        self.assertEqual(evaluate_vendor_sla(4.2, 0.05), "Compliant")
        self.assertEqual(evaluate_vendor_sla(3.8, 0.05), "Non-Compliant") # Rating breach
        self.assertEqual(evaluate_vendor_sla(4.1, 0.12), "Non-Compliant") # Negative ratio breach
        self.assertEqual(evaluate_vendor_sla(3.2, 0.25), "Non-Compliant") # Both breached

    def test_tc_t_08_correlation_calculation(self):
        """TC-T-08: Verify Pearson correlation computation bounds and accuracy."""
        x = [1, 2, 3, 4, 5]
        y = [1.2, 2.1, 2.9, 4.1, 5.0]
        
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y))
        r = cov / (std_x * std_y)
        
        self.assertGreaterEqual(r, -1.0)
        self.assertLessEqual(r, 1.0)
        self.assertGreater(r, 0.95, "Expected strong positive correlation for monotonic sequence")

if __name__ == "__main__":
    unittest.main()
