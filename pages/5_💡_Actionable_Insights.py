"""
Page 5: Actionable Insights & Prescriptive Engine (BUILD-12)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import streamlit as st
import pandas as pd
import numpy as np
import src.data_loader as data_loader
import src.sentiment as sentiment
import src.ui as ui

try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = data_loader.load_analytics_data()

df = st.session_state["df_filtered"]

ui.render_tailwind_header(
    "Actionable Insights & Prescriptive Operations",
    "Sarcasm Divergence, Root-Cause Defect Taxonomy & Operational Interventions (OQ-03, OQ-05, BR-04, BR-05, BR-11)",
    "Prescriptive Engine"
)

# 1. Sarcastic & Divergent Review Flagging
st.markdown("### 🎭 Sarcasm & Sentiment Divergence Moderation Queue (OQ-03)")
st.caption("Reviews exhibiting sharp polarity mismatches (e.g. 5-star ratings with biting negative commentary requiring manual moderation)")

divergent_df = sentiment.flag_sentiment_divergence(df)
st.markdown(f"**Total Divergent Reviews Detected:** `{len(divergent_df)}` records")

if not divergent_df.empty:
    display_cols = ["review_id", "product_name", "rating", "sentiment_score", "divergence_type", "review_title", "review_text", "moderation_status"]
    available_cols = [c for c in display_cols if c in divergent_df.columns]
    st.dataframe(divergent_df[available_cols], use_container_width=True, hide_index=True)
else:
    st.success("Zero sentiment divergence flags in active filter selection.")

ui.render_insight_box(
    "Sarcasm Moderation Policy",
    "Sarcastic reviews misrepresent true product health in star rating aggregates. Routing these 18 reviews to customer support prevents silent customer churn.",
    "warning"
)

st.markdown("---")

# 2. Defect Root-Cause Taxonomy
col_d1, col_d2 = st.columns([1, 1])

with col_d1:
    st.markdown("### 🛠️ Primary Defect Tag Frequency Pareto")
    st.caption("Breakdown of engineering and logistics defects reported in 1-star & 2-star reviews")

    defect_counts = sentiment.extract_top_defect_keywords(df)
    if not defect_counts.empty:
        if HAS_PLOTLY:
            fig_def = px.bar(
                defect_counts,
                x="count",
                y="primary_defect_tag",
                orientation="h",
                text="percentage",
                color="primary_defect_tag",
                title="Negative Review Defect Frequency",
                color_discrete_sequence=["#DC2626", "#EA580C", "#D97706", "#2563EB", "#64748B"]
            )
            fig_def.update_traces(texttemplate="%{text}%", textposition="outside")
            ui.apply_plotly_theme(fig_def)
            st.plotly_chart(fig_def, use_container_width=True)
        else:
            st.dataframe(defect_counts, use_container_width=True, hide_index=True)
    else:
        st.info("No negative defect records in selected view.")

with col_d2:
    st.markdown("### 📋 Automated Prescriptive Action Matrix")
    st.caption("Algorithmically generated operational interventions based on live defect clusters (BR-11)")

    actions = sentiment.get_prescriptive_actions(df)
    for act in actions:
        with st.expander(f"📌 [{act['priority']}] {act['domain']}", expanded=True):
            st.markdown(f"**Trigger:** `{act['trigger']}`")
            st.markdown(f"**Operational Recommendation:** {act['recommendation']}")
            st.markdown(f"**Commercial Impact:** *{act['impact']}*")
