"""
Data Loader & SQLite Access Layer (BUILD-02)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

# Decorate with st.cache_data if streamlit is installed
try:
    import streamlit as st
    cache_decorator = st.cache_data
except ImportError:
    def cache_decorator(func):
        return func

@cache_decorator
def load_analytics_data(db_path=DB_PATH) -> pd.DataFrame:
    """
    Loads the joined 38-column view_review_analytics dataset from SQLite.
    Applies data type casting for dates and numerics.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"SQLite database not found at {db_path}")

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM view_review_analytics;"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert date and timestamp columns
    if "review_date" in df.columns:
        df["review_date"] = pd.to_datetime(df["review_date"])
    if "review_timestamp" in df.columns:
        df["review_timestamp"] = pd.to_datetime(df["review_timestamp"])

    # Ensure numeric columns are strictly typed
    numeric_cols = ["rating", "sentiment_score", "helpful_votes", "review_length_words",
                    "price", "product_cost", "age", "return_intent_flag",
                    "rating_sentiment_divergence", "is_verified_purchase"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Extracts available categorical values and bounds for sidebar filters.
    """
    categories = sorted(df["category_name"].dropna().unique().tolist()) if "category_name" in df.columns else []
    vendors = sorted(df["vendor_name"].dropna().unique().tolist()) if "vendor_name" in df.columns else []
    
    min_date = df["review_date"].min().date() if "review_date" in df.columns and not df.empty else None
    max_date = df["review_date"].max().date() if "review_date" in df.columns and not df.empty else None

    return {
        "categories": categories,
        "vendors": vendors,
        "min_date": min_date,
        "max_date": max_date,
        "rating_range": (1, 5)
    }

def filter_reviews(df: pd.DataFrame,
                   categories=None,
                   vendors=None,
                   date_range=None,
                   min_rating: int = 1,
                   max_rating: int = 5,
                   verified_only: bool = False) -> pd.DataFrame:
    """
    Filters the reporting dataset reactively based on user sidebar controls.
    """
    filtered = df.copy()

    # Category filter
    if categories:
        if isinstance(categories, str):
            categories = [categories]
        filtered = filtered[filtered["category_name"].isin(categories)]

    # Vendor filter
    if vendors:
        if isinstance(vendors, str):
            vendors = [vendors]
        filtered = filtered[filtered["vendor_name"].isin(vendors)]

    # Date range filter
    if date_range and len(date_range) == 2 and date_range[0] and date_range[1]:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["review_date"] >= start_date) & (filtered["review_date"] <= end_date)]

    # Star rating bounds
    filtered = filtered[(filtered["rating"] >= min_rating) & (filtered["rating"] <= max_rating)]

    # Verified buyer filter
    if verified_only:
        filtered = filtered[filtered["is_verified_purchase"] == 1]

    return filtered

if __name__ == "__main__":
    data = load_analytics_data()
    opts = get_filter_options(data)
    print(f"Loaded {len(data)} rows and {len(data.columns)} columns.")
    print(f"Categories ({len(opts['categories'])}): {opts['categories']}")
    print(f"Date range: {opts['min_date']} to {opts['max_date']}")
