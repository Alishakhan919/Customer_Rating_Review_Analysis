"""
Test Suite: Application Infrastructure, Performance & UI Rendering (TC-T-05, TC-T-11, TC-T-12)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import os
import sys
import time
import sqlite3
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
CONFIG_PATH = os.path.join(BASE_DIR, ".streamlit", "config.toml")
UI_LIB_PATH = os.path.join(BASE_DIR, "src", "ui.py")

class TestAppInfrastructure(unittest.TestCase):

    def test_tc_t_05_database_load_latency(self):
        """TC-T-05: Verify data loading from data/app.db executes in under 3.0 seconds."""
        self.assertTrue(os.path.exists(DB_PATH), f"Database missing at {DB_PATH}")
        
        start_time = time.perf_counter()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Query entire joined analytics view
        cursor.execute("SELECT * FROM view_review_analytics;")
        records = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        conn.close()
        elapsed_time = time.perf_counter() - start_time
        
        self.assertGreater(len(records), 150, "Expected at least 150 records in analytics view")
        self.assertLess(elapsed_time, 3.0, f"Query execution latency ({elapsed_time:.4f}s) exceeded 3.0s SLA")

    def test_tc_t_11_theme_configuration_integrity(self):
        """TC-T-11: Verify .streamlit/config.toml contains enterprise theme definitions."""
        self.assertTrue(os.path.exists(CONFIG_PATH), f"Config missing at {CONFIG_PATH}")
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("[theme]", content)
        self.assertIn("primaryColor", content)
        self.assertIn("#1B365D", content, "Expected primary blue #1B365D in theme config")
        self.assertIn("backgroundColor", content)

    def test_tc_t_12_ui_component_generator(self):
        """TC-T-12: Verify Tailwind HTML components generation and CDN presence."""
        self.assertTrue(os.path.exists(UI_LIB_PATH), f"UI component library missing at {UI_LIB_PATH}")
        
        # Add src directory to path if not present
        src_dir = os.path.join(BASE_DIR, "src")
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
            
        try:
            import ui
            header_html = ui.render_tailwind_header("Executive Test", "Subtitle Test")
            self.assertIn("https://cdn.tailwindcss.com", header_html)
            self.assertIn("Executive Test", header_html)
            
            kpi_html = ui.render_kpi_card("Mean Rating", "4.2", "+0.3 vs LY", "positive", "⭐")
            self.assertIn("https://cdn.tailwindcss.com", kpi_html)
            self.assertIn("Mean Rating", kpi_html)
            self.assertIn("4.2", kpi_html)
        except (ImportError, ModuleNotFoundError) as e:
            self.skipTest(f"Streamlit or UI dependency pending build (Step 15): {e}")

    def test_tc_t_13_streamlit_apptest_readiness(self):
        """TC-T-13: Streamlit AppTest harness readiness check for multipage navigation."""
        try:
            from streamlit.testing.v1 import AppTest
            self.assertTrue(callable(AppTest.from_file) or hasattr(AppTest, "from_file"))
        except ImportError:
            # Mark as pending Step 15 when streamlit finishes installing
            self.skipTest("Streamlit not yet installed or wheel download in progress; ready for Step 15 build")

if __name__ == "__main__":
    unittest.main()
