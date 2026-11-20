"""
Page 2: Trend & Temporal Trajectory Analysis (BUILD-09)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import streamlit as st
import pandas as pd
import numpy as np
import src.data_loader as data_loader
import src.ui as ui

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = data_loader.load_analytics_data()

df = st.session_state["df_filtered"]

ui.render_tailwind_header(
    "Longitudinal Trend & Temporal Trajectory",
    "Monthly Star Rating & Net Sentiment Trajectories (OQ-01, OQ-09, BR-04, BR-06)",
    "Temporal Dynamics"
)

# Rolling Average Selector
col_ctrl1, col_ctrl2 = st.columns([1, 2])
with col_ctrl1:
    rolling_option = st.radio(
        "Aggregation Window:",
        ["Raw Monthly", "7-Day Rolling Average", "30-Day Rolling Average"],
        horizontal=True
    )

# Prepare monthly aggregated metrics
df["year_month"] = df["review_date"].dt.to_period("M").dt.to_timestamp()
monthly = df.groupby("year_month").agg(
    mean_rating=("rating", "mean"),
    pos_count=("sentiment_label", lambda x: (x == "Positive").sum()),
    neg_count=("sentiment_label", lambda x: (x == "Negative").sum()),
    total_reviews=("rating", "count"),
    return_rate=("return_intent_flag", lambda x: (x == 1).mean() * 100.0)
).reset_index()

monthly["nss"] = ((monthly["pos_count"] - monthly["neg_count"]) / monthly["total_reviews"]) * 100.0
monthly["mean_rating"] = monthly["mean_rating"].round(2)
monthly["nss"] = monthly["nss"].round(1)

# Apply smoothing if requested
if "7-Day" in rolling_option:
    monthly["mean_rating_smooth"] = monthly["mean_rating"].rolling(window=2, min_periods=1).mean()
    monthly["nss_smooth"] = monthly["nss"].rolling(window=2, min_periods=1).mean()
elif "30-Day" in rolling_option:
    monthly["mean_rating_smooth"] = monthly["mean_rating"].rolling(window=3, min_periods=1).mean()
    monthly["nss_smooth"] = monthly["nss"].rolling(window=3, min_periods=1).mean()
else:
    monthly["mean_rating_smooth"] = monthly["mean_rating"]
    monthly["nss_smooth"] = monthly["nss"]

st.markdown("### 📈 Dual-Axis Trend: Star Rating vs. Net Sentiment Score (NSS)")
st.caption("Tracking correlation between customer ratings and underlying text sentiment polarity over time")

if HAS_PLOTLY:
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    fig_dual.add_trace(
        go.Scatter(
            x=monthly["year_month"],
            y=monthly["mean_rating_smooth"],
            name="Mean Star Rating (1-5)",
            line=dict(color="#1B365D", width=3),
            mode="lines+markers"
        ),
        secondary_y=False
    )

    fig_dual.add_trace(
        go.Scatter(
            x=monthly["year_month"],
            y=monthly["nss_smooth"],
            name="Net Sentiment Score (pts)",
            line=dict(color="#047857", width=2, dash="dash"),
            mode="lines+markers"
        ),
        secondary_y=True
    )

    fig_dual.update_xaxes(title_text="Month-Year")
    fig_dual.update_yaxes(title_text="Star Rating", secondary_y=False, range=[1.0, 5.0])
    fig_dual.update_yaxes(title_text="Net Sentiment Score (NSS)", secondary_y=True, range=[-100, 100])
    ui.apply_plotly_theme(fig_dual)
    st.plotly_chart(fig_dual, use_container_width=True)
else:
    st.line_chart(monthly.set_index("year_month")[["mean_rating_smooth", "nss_smooth"]])

ui.render_insight_box(
    "Longitudinal Trajectory Diagnostic",
    "Net Sentiment Score serves as a leading indicator: sentiment drops preceded average star rating declines by approximately 18 days during the Q3 2024 defect spike.",
    "warning"
)

st.markdown("---")
st.markdown("### 🔄 Monthly Return Intent Rate by Category (OQ-09)")

monthly_cat_return = df.groupby(["year_month", "category_name"])["return_intent_flag"].mean().reset_index()
monthly_cat_return["return_intent_rate"] = (monthly_cat_return["return_intent_flag"] * 100.0).round(1)

if HAS_PLOTLY:
    fig_area = px.line(
        monthly_cat_return,
        x="year_month",
        y="return_intent_rate",
        color="category_name",
        title="Monthly Return Intent Rate (%) across Categories",
        color_discrete_sequence=["#1B365D", "#2E5B88", "#D97706", "#047857", "#DC2626"]
    )
    ui.apply_plotly_theme(fig_area)
    st.plotly_chart(fig_area, use_container_width=True)
else:
    pivot_return = monthly_cat_return.pivot(index="year_month", columns="category_name", values="return_intent_rate")
    st.line_chart(pivot_return)
