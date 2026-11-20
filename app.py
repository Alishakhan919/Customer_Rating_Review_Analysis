"""
Customer Rating & Review Analysis (CRRA) - Enterprise Portal (BUILD-07)
Application Entry Point & Multipage Orchestrator
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import os
import sys
import pandas as pd

# Add project root and src to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
src_dir = os.path.join(BASE_DIR, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

import src.data_loader as data_loader
import src.cleaning as cleaning
import src.analytics as analytics
import src.ui as ui

def init_session_state():
    """Initializes global session state attributes and cached data."""
    if "df_raw" not in st.session_state:
        df_raw = data_loader.load_analytics_data()
        df_clean, quality_report = cleaning.clean_review_data(df_raw)
        st.session_state["df_raw"] = df_raw
        st.session_state["df_clean"] = df_clean
        st.session_state["quality_report"] = quality_report
        st.session_state["filter_options"] = data_loader.get_filter_options(df_clean)

def render_sidebar():
    """Renders persistent global filters in the sidebar."""
    st.sidebar.markdown(
        """
        <div style="padding: 10px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 15px;">
            <h2 style="color: #1B365D; margin: 0; font-size: 1.25rem; font-weight: 800;">🛍️ NexCart CRRA</h2>
            <p style="color: #64748B; margin: 0; font-size: 0.75rem;">Enterprise Analytics Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    opts = st.session_state["filter_options"]
    df_clean = st.session_state["df_clean"]

    # Filter Controls
    st.sidebar.markdown("### 🔍 Global Data Filters")
    
    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=opts["categories"],
        default=opts["categories"],
        help="Filter across D2C retail product categories"
    )

    selected_vendors = st.sidebar.multiselect(
        "Marketplace Vendor",
        options=opts["vendors"],
        default=[],
        help="Filter reviews by specific 3P vendors (Leave empty for all)"
    )

    min_date = opts["min_date"]
    max_date = opts["max_date"]
    selected_date_range = st.sidebar.date_input(
        "Review Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter customer feedback across time windows"
    )

    rating_range = st.sidebar.slider(
        "Star Rating Bounds",
        min_value=1,
        max_value=5,
        value=(1, 5),
        help="Filter reviews by star rating tier"
    )

    verified_only = st.sidebar.checkbox(
        "Verified Purchases Only",
        value=False,
        help="Filter to authentic verified customer reviews"
    )

    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    # Apply Filters
    df_filtered = data_loader.filter_reviews(
        df_clean,
        categories=selected_categories if selected_categories else None,
        vendors=selected_vendors if selected_vendors else None,
        date_range=selected_date_range if isinstance(selected_date_range, (list, tuple)) and len(selected_date_range) == 2 else None,
        min_rating=rating_range[0],
        max_rating=rating_range[1],
        verified_only=verified_only
    )
    st.session_state["df_filtered"] = df_filtered

    # Active filter status summary in sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Dataset Grain:** `{len(df_filtered)}` of `{len(df_clean)}` reviews")
    st.sidebar.markdown(f"**Cleanliness:** `{st.session_state['quality_report']['cleanliness_score_pct']}%` Clean")
    st.sidebar.caption("Author: Alisha Khan (2503201450012)")

def main():
    if not HAS_STREAMLIT:
        print("Streamlit not installed in current environment.")
        return

    st.set_page_config(
        page_title="NexCart CRRA Intelligence",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    init_session_state()
    render_sidebar()

    df_filtered = st.session_state.get("df_filtered", st.session_state["df_clean"])

    # Header
    ui.render_tailwind_header(
        "Customer Rating & Review Analysis (CRRA)",
        "Executive Decision Support & Operational Intelligence Portal | NexCart Retail Solutions Pvt. Ltd.",
        "Production V1.0"
    )

    # Empty Filter Defensive Guard (TC-F-14)
    if df_filtered.empty:
        st.warning("⚠️ No customer reviews match your selected filter criteria. Please broaden your selection or reset filters.")
        if st.button("Reset Global Filters to Default"):
            st.rerun()
        st.stop()

    # Executive Overview Metrics
    kpis = analytics.compute_executive_kpis(df_filtered)
    kpi_cards = [
        {"label": "Total Review Volume", "value": f"{kpis['total_reviews']:,}", "sub": "100% Ingested", "trend": "Active Records", "status": "neutral", "icon": "📝"},
        {"label": "Average Star Rating", "value": f"{kpis['mean_rating']:.2f} ★", "sub": "Target: 4.0 ★", "trend": f"{kpis['mean_rating'] - 4.0:+.2f} Gap", "status": "positive" if kpis['mean_rating'] >= 4.0 else "warning", "icon": "⭐"},
        {"label": "Net Sentiment Score", "value": f"{kpis['net_sentiment_score']:+.1f}", "sub": "NSS Benchmark > +30", "trend": "Polarity Lift", "status": "positive" if kpis['net_sentiment_score'] >= 30 else "warning", "icon": "📈"},
        {"label": "Return Intent Rate", "value": f"{kpis['return_intent_rate']:.1f}%", "sub": "SLA Ceil: < 15.0%", "trend": "High Return Alert" if kpis['return_intent_rate'] > 15 else "Controlled", "status": "critical" if kpis['return_intent_rate'] > 15 else "positive", "icon": "🔄"}
    ]
    ui.render_kpi_cards(kpi_cards)

    # Multi-Page Navigation Hub
    st.markdown("### 🗺️ Multi-Page Operational Modules")
    st.markdown("Navigate through specialized analytical pages using the sidebar menu or quick links below:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **01. Executive Overview**\n\nExecutive KPI dashboard, bimodal J-curve rating distributions, and category health benchmarks.")
        st.warning("📈 **02. Trend Analysis**\n\nMonthly dual-axis trajectories, 7/30-day rolling averages, and seasonal engagement spikes.")
    with col2:
        st.error("🏢 **03. Vendor Comparison**\n\nMarketplace vendor defect risk quadrant, 4.0 SLA breach penalties, and supplier scorecards.")
        st.success("🔬 **04. Statistical Tests & EDA**\n\nWelch's two-sample t-test (Verified vs Unverified), Chi-square defect tests, and 7x24 temporal heatmaps.")
    with col3:
        st.info("💡 **05. Actionable Insights**\n\nSarcasm & sentiment divergence detection, defect taxonomy, and automated prescriptive action matrix.")
        st.info("📥 **06. Data Explorer & Export**\n\nInteractive 38-column analytical grid with search, multi-column sorting, and filtered CSV export.")

    st.markdown("---")
    
    # Operational Questions Coverage Table
    st.markdown("### 🎯 Operational Questions (OQ-01 through OQ-10) Traceability")
    oq_data = [
        {"OQ": "OQ-01", "Core Question": "How are customer ratings distributed across the product catalog?", "Page": "01_📊_Executive_Overview", "Method": "Bimodal J-Curve Histogram & Share Breakdown"},
        {"OQ": "OQ-02", "Core Question": "Which product SKUs suffer from severe negative ratings?", "Page": "03_🏢_Vendor_Comparison", "Method": "SKU Defect Flagging & Low-Rating Pareto"},
        {"OQ": "OQ-03", "Core Question": "Do star ratings accurately reflect textual review sentiment?", "Page": "05_💡_Actionable_Insights", "Method": "Sentiment Polarity vs Rating Divergence Matrix"},
        {"OQ": "OQ-04", "Core Question": "Are unverified buyer ratings significantly lower than verified?", "Page": "04_🔬_Statistical_Tests", "Method": "Welch's Two-Sample t-Test (p < 0.001)"},
        {"OQ": "OQ-05", "Core Question": "What are the primary defect categories driving customer returns?", "Page": "04_🔬_Statistical_Tests & 05", "Method": "Chi-Square Test & Prescriptive Matrix"},
        {"OQ": "OQ-06", "Core Question": "How do marketplace vendors perform against the 4.0 star SLA?", "Page": "03_🏢_Vendor_Comparison", "Method": "Vendor Defect Risk Quadrant Scatter Plot"},
        {"OQ": "OQ-07", "Core Question": "Which reviews receive the highest helpful votes?", "Page": "06_📥_Data_Explorer", "Method": "Helpfulness Social Influence Ranking"},
        {"OQ": "OQ-08", "Core Question": "How do demographic cohorts differ in product satisfaction?", "Page": "04_🔬_Statistical_Tests", "Method": "Age Group & Regional Satisfaction Cross-Tabs"},
        {"OQ": "OQ-09", "Core Question": "What customer intent signals indicate imminent returns?", "Page": "02_📈_Trend_Analysis", "Method": "Regex Return Intent Trajectory Mapping"},
        {"OQ": "OQ-10", "Core Question": "What is the optimal temporal window for review engagement?", "Page": "04_🔬_Statistical_Tests", "Method": "7x24 Day-of-Week vs Hour Peak Heatmap"}
    ]
    st.dataframe(pd.DataFrame(oq_data), use_container_width=True, hide_index=True)

    # Footer
    st.markdown("---")
    st.caption("NexCart CRRA Intelligence Platform | Alisha Khan (Roll No. 2503201450012) | ABES Engineering College, Ghaziabad")

if __name__ == "__main__":
    main()
