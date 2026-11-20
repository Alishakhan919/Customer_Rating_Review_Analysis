"""
Sentiment Polarity, Sarcasm Divergence & Intent Extraction (BUILD-05)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import re
import pandas as pd

RETURN_INTENT_PATTERN = re.compile(
    r'\b(return|returned|returning|refund|replace|replacement|defective|damaged|broken|dead)\b',
    re.IGNORECASE
)

def detect_return_intent(text: str) -> int:
    """
    Returns 1 if customer review contains explicit return, refund, or defect keywords.
    """
    if not isinstance(text, str):
        return 0
    return 1 if bool(RETURN_INTENT_PATTERN.search(text)) else 0

def flag_sentiment_divergence(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags reviews exhibiting rating-sentiment divergence:
    - Sarcastic Praise: High rating (>= 4) but negative sentiment score (<= -0.2)
    - Polite Complaint: Low rating (<= 2) but positive sentiment score (>= 0.2)
    """
    if df.empty or "rating" not in df.columns or "sentiment_score" not in df.columns:
        return pd.DataFrame()

    sarcastic_mask = (df["rating"] >= 4) & (df["sentiment_score"] <= -0.2)
    polite_mask = (df["rating"] <= 2) & (df["sentiment_score"] >= 0.2)

    divergent = df[sarcastic_mask | polite_mask].copy()
    divergent["divergence_type"] = "Sarcastic Praise (Rating >= 4, Neg Sent)"
    divergent.loc[polite_mask, "divergence_type"] = "Polite Complaint (Rating <= 2, Pos Sent)"
    divergent["moderation_status"] = "Action Required (Manual Audit)"

    return divergent

def extract_top_defect_keywords(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Aggregates defect tags from 1-star and 2-star reviews.
    """
    if df.empty or "rating" not in df.columns or "primary_defect_tag" not in df.columns:
        return pd.DataFrame(columns=["primary_defect_tag", "count", "percentage"])

    neg_df = df[df["rating"] <= 2]
    if neg_df.empty:
        return pd.DataFrame(columns=["primary_defect_tag", "count", "percentage"])

    counts = neg_df["primary_defect_tag"].value_counts().reset_index()
    counts.columns = ["primary_defect_tag", "count"]
    counts["percentage"] = (counts["count"] / len(neg_df) * 100.0).round(1)
    return counts.head(top_n)

def get_prescriptive_actions(df: pd.DataFrame) -> list[dict]:
    """
    Evaluates current dataset patterns and generates prioritized operational action recommendations.
    """
    actions = []
    if df.empty:
        return actions

    # 1. Product Defect Inspection (ELEC-104 or Battery Defect Cluster)
    battery_issues = df[(df["primary_defect_tag"] == "Battery Defect") & (df["rating"] <= 2)]
    if len(battery_issues) >= 5:
        actions.append({
            "priority": "Critical (P1)",
            "domain": "Product Engineering & Quality",
            "trigger": f"Detected {len(battery_issues)} negative reviews citing Battery Defect in Electronics",
            "recommendation": "Immediately halt batch shipments for SKU ELEC-104. Trigger formal engineering supplier audit with battery cell manufacturer.",
            "impact": "Mitigates estimated 18% return surge and prevents catalog brand erosion."
        })

    # 2. Packaging / Logistics Damage
    pkg_issues = df[(df["primary_defect_tag"] == "Damaged Packaging") & (df["rating"] <= 2)]
    if len(pkg_issues) >= 3:
        actions.append({
            "priority": "High (P2)",
            "domain": "Logistics & Fulfillment",
            "trigger": f"Detected {len(pkg_issues)} packaging damage complaints during transit",
            "recommendation": "Review 3PL courier drop tests. Mandate reinforced corrugated outer boxes for fragile Home & Kitchen SKUs.",
            "impact": "Projected 35% reduction in transit-related return replacement requests."
        })

    # 3. Vendor SLA Breaches
    if "vendor_name" in df.columns:
        vendor_ratings = df.groupby("vendor_name")["rating"].mean()
        breached_vendors = vendor_ratings[vendor_ratings < 4.0].index.tolist()
        if breached_vendors:
            actions.append({
                "priority": "High (P2)",
                "domain": "Vendor Relationship Management",
                "trigger": f"Vendors below 4.0 star SLA benchmark: {', '.join(breached_vendors[:3])}",
                "recommendation": "Issue formal breach cure notices. Enforce contractual 3% marketplace commission penalty until rating recovers.",
                "impact": "Protects marketplace consumer trust and drives vendor compliance."
            })

    # 4. Sarcastic Review Flagging
    sarcastic = df[(df["rating"] >= 4) & (df["sentiment_score"] <= -0.2)]
    if len(sarcastic) >= 2:
        actions.append({
            "priority": "Medium (P3)",
            "domain": "Customer Experience & Moderation",
            "trigger": f"Flagged {len(sarcastic)} reviews with high rating but sharply negative sentiment",
            "recommendation": "Route sarcastic reviews to Tier-2 support team to proactively contact customers and offer resolution.",
            "impact": "Converts alienated sarcastic customers into retained brand advocates."
        })

    return actions

if __name__ == "__main__":
    from data_loader import load_analytics_data
    df = load_analytics_data()
    div = flag_sentiment_divergence(df)
    print(f"Flagged {len(div)} divergent reviews.")
    acts = get_prescriptive_actions(df)
    print(f"Generated {len(acts)} prescriptive actions:")
    for a in acts:
        print(f"  [{a['priority']}] {a['trigger']}")
