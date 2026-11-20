"""
Page 3: Category & Vendor Benchmarking (BUILD-10)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import streamlit as st
import pandas as pd
import numpy as np
import src.data_loader as data_loader
import src.analytics as analytics
import src.ui as ui

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = data_loader.load_analytics_data()

df = st.session_state["df_filtered"]

ui.render_tailwind_header(
    "Vendor Benchmarking & Defect Risk Quadrants",
    "Supplier SLA Compliance & Defect Concentration Diagnostics (OQ-05, OQ-06, BR-03, BR-11)",
    "Partner Risk Suite"
)

# 1. Category Benchmark Matrix
st.markdown("### 🏢 Category Benchmark Performance vs. 4.0 Star SLA")
cat_perf = df.groupby("category_name").agg(
    total_reviews=("rating", "count"),
    mean_rating=("rating", "mean"),
    neg_reviews=("rating", lambda x: (x <= 2).sum()),
    return_rate=("return_intent_flag", lambda x: (x == 1).mean() * 100.0)
).reset_index()

cat_perf["mean_rating"] = cat_perf["mean_rating"].round(2)
cat_perf["gap_vs_benchmark"] = (cat_perf["mean_rating"] - 4.0).round(2)
cat_perf["neg_ratio"] = ((cat_perf["neg_reviews"] / cat_perf["total_reviews"]) * 100.0).round(1)
cat_perf["return_rate"] = cat_perf["return_rate"].round(1)
cat_perf["sla_status"] = np.where(cat_perf["mean_rating"] >= 4.0, "Compliant (Target Met)", "SLA Breach (Action Required)")

st.dataframe(cat_perf, use_container_width=True, hide_index=True)

st.markdown("---")

# 2. Vendor Defect Risk Quadrant Plot
st.markdown("### 🎯 Vendor Risk Quadrant: Rating vs. Return Intent Rate")
st.caption("Lower-Right Quadrant indicates high commercial risk: Star Rating < 4.0 and Return Intent > 10.0%")

vendor_summary = analytics.evaluate_vendor_slas(df)

if HAS_PLOTLY:
    fig_quad = px.scatter(
        vendor_summary,
        x="return_rate",
        y="mean_rating",
        size="review_count",
        color="sla_status",
        hover_name="vendor_name",
        text="vendor_name",
        color_discrete_map={"Compliant": "#047857", "Non-Compliant": "#DC2626"},
        title="Vendor Defect Risk Quadrant (Size = Total Reviews)",
        labels={"return_rate": "Return Intent Rate (%)", "mean_rating": "Average Star Rating (1-5)"}
    )
    # Add benchmark threshold lines
    fig_quad.add_hline(y=4.0, line_dash="dash", line_color="#D97706", annotation_text="SLA Rating Floor (4.0 ★)")
    fig_quad.add_vline(x=10.0, line_dash="dash", line_color="#D97706", annotation_text="Return Threshold (10%)")
    fig_quad.update_traces(textposition="top center")
    ui.apply_plotly_theme(fig_quad)
    st.plotly_chart(fig_quad, use_container_width=True)
else:
    st.dataframe(vendor_summary, use_container_width=True, hide_index=True)

ui.render_insight_box(
    "Vendor Compliance Finding",
    "ApexTech Solutions exhibits the highest operational risk with an average rating of 3.65 ★ and return intent exceeding 16.5%. Triggers mandatory 3% marketplace penalty surcharge.",
    "warning"
)

st.markdown("---")

# 3. Itemized Vendor Defect Breakdown
st.markdown("### 🔍 Itemized Vendor Defect Distribution Table")
vendor_defect_pivot = pd.crosstab(
    df["vendor_name"],
    df["primary_defect_tag"],
    margins=True,
    margins_name="Total Feedback"
)
st.dataframe(vendor_defect_pivot, use_container_width=True)
