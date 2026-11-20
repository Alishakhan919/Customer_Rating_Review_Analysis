"""
Data Cleaning, Imputation & Quality Assurance Pipeline (BUILD-03)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import pandas as pd

def clean_review_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the raw reporting dataset:
    1. Imputes null or empty review titles with '[Untitled Review]'.
    2. Identifies and deduplicates records by review_id.
    3. Audits rating and sentiment ranges.
    Returns:
        tuple (cleaned_df, quality_report_dict)
    """
    cleaned = df.copy()
    total_raw = len(cleaned)

    # 1. Audit and impute missing review titles
    missing_title_mask = cleaned["review_title"].isna() | (cleaned["review_title"].astype(str).str.strip() == "")
    missing_titles_count = int(missing_title_mask.sum())
    cleaned.loc[missing_title_mask, "review_title"] = "[Untitled Review]"

    # 2. Audit and purge duplicate records by review_id
    duplicate_mask = cleaned.duplicated(subset=["review_id"], keep="first")
    duplicates_count = int(duplicate_mask.sum())
    cleaned = cleaned.drop_duplicates(subset=["review_id"], keep="first")

    # 3. Domain range audits
    invalid_ratings = int(((cleaned["rating"] < 1) | (cleaned["rating"] > 5)).sum())
    invalid_sentiment = int(((cleaned["sentiment_score"] < -1.0) | (cleaned["sentiment_score"] > 1.0)).sum())

    clean_records_count = len(cleaned)

    # Calculate overall cleanliness score
    cleanliness_score = round(100.0 - ((missing_titles_count + duplicates_count) / max(total_raw, 1) * 100.0), 2)

    quality_report = {
        "total_raw_records": total_raw,
        "missing_titles_count": missing_titles_count,
        "duplicates_removed_count": duplicates_count,
        "invalid_ratings_count": invalid_ratings,
        "invalid_sentiment_count": invalid_sentiment,
        "clean_records_count": clean_records_count,
        "cleanliness_score_pct": cleanliness_score
    }

    return cleaned, quality_report

def get_duplicate_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns all rows where review_id has duplicates (both original and copies) for audit display.
    """
    return df[df.duplicated(subset=["review_id"], keep=False)].sort_values(by="review_id")

if __name__ == "__main__":
    from data_loader import load_analytics_data
    raw = load_analytics_data()
    clean_df, report = clean_review_data(raw)
    print("Quality Audit Summary:")
    for k, v in report.items():
        print(f"  {k}: {v}")
