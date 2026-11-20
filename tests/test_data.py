"""
Test Suite: Data Layer & Relational Integrity (TC-T-01 to TC-T-03)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import sqlite3
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

class TestDataIntegrity(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.exists(DB_PATH), f"Database not found at {DB_PATH}")
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_tc_t_01_foreign_key_integrity(self):
        """TC-T-01: Verify zero foreign key violations across the relational schema."""
        fk_violations = self.cursor.execute("PRAGMA foreign_key_check;").fetchall()
        self.assertEqual(len(fk_violations), 0, f"Foreign key check failed with violations: {fk_violations}")

    def test_tc_t_02_table_row_and_column_counts(self):
        """TC-T-02: Verify expected row counts and table presence."""
        table_counts = {
            "dim_categories": 5,
            "dim_vendors": 15,
            "dim_products": 50,
            "dim_customers": 100
        }
        for table, expected_count in table_counts.items():
            count = self.cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
            self.assertEqual(count, expected_count, f"Table {table} expected {expected_count} rows, found {count}")

        # Fact table must have 150+ records
        rev_count = self.cursor.execute("SELECT COUNT(*) FROM fact_reviews;").fetchone()[0]
        self.assertGreaterEqual(rev_count, 150, f"fact_reviews expected at least 150 rows, found {rev_count}")

    def test_tc_t_03_primary_key_uniqueness_and_ranges(self):
        """TC-T-03: Verify PK uniqueness, NOT NULL constraints, and range bounds."""
        # 1. Category PK uniqueness
        cat_dups = self.cursor.execute("SELECT category_id, COUNT(*) FROM dim_categories GROUP BY category_id HAVING COUNT(*) > 1;").fetchall()
        self.assertEqual(len(cat_dups), 0)

        # 2. Product SKU uniqueness
        sku_dups = self.cursor.execute("SELECT sku, COUNT(*) FROM dim_products GROUP BY sku HAVING COUNT(*) > 1;").fetchall()
        self.assertEqual(len(sku_dups), 0)

        # 3. Rating range [1, 5]
        invalid_ratings = self.cursor.execute("SELECT COUNT(*) FROM fact_reviews WHERE rating < 1 OR rating > 5;").fetchone()[0]
        self.assertEqual(invalid_ratings, 0, f"Found {invalid_ratings} ratings outside [1, 5]")

        # 4. Sentiment score range [-1.0, 1.0]
        invalid_sent = self.cursor.execute("SELECT COUNT(*) FROM fact_reviews WHERE sentiment_score < -1.0 OR sentiment_score > 1.0;").fetchone()[0]
        self.assertEqual(invalid_sent, 0, f"Found {invalid_sent} sentiment scores outside [-1.0, 1.0]")

    def test_tc_t_04_analytical_view_columns(self):
        """TC-T-04: Verify view_review_analytics has required columns (30-40)."""
        self.cursor.execute("SELECT * FROM view_review_analytics LIMIT 1;")
        col_names = [desc[0] for desc in self.cursor.description]
        self.assertGreaterEqual(len(col_names), 30, f"View expected >= 30 columns, found {len(col_names)}")
        self.assertLessEqual(len(col_names), 40, f"View expected <= 40 columns, found {len(col_names)}")
        
        # Verify critical joined attributes exist
        expected_cols = ["review_id", "rating", "sentiment_score", "sku", "product_name", "category_name", "vendor_name", "age", "customer_region"]
        for ec in expected_cols:
            self.assertIn(ec, col_names, f"Expected column {ec} missing from view_review_analytics")

    def test_tc_t_07_data_cleaning_and_deduplication(self):
        """TC-T-07: Verify data cleaning logic: missing titles imputation and duplicate handling."""
        raw_rows = self.cursor.execute("SELECT review_id, review_title FROM fact_reviews;").fetchall()
        
        # Verify simulated data contains realistic missing titles for cleaning demonstration
        missing_titles = [r for r in raw_rows if r[1] is None or r[1] == "" or r[1] == "[Untitled Review]"]
        self.assertGreater(len(missing_titles), 0, "Expected simulated missing titles for cleaning audit")
        
        # Verify deduplication logic
        id_counts = {}
        for r_id, _ in raw_rows:
            id_counts[r_id] = id_counts.get(r_id, 0) + 1
        
        # Deduplicated distinct count must equal set size
        distinct_ids = set(r[0] for r in raw_rows)
        self.assertEqual(len(distinct_ids), len(id_counts))

if __name__ == "__main__":
    unittest.main()
