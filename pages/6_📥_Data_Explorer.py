"""
Page 6: Data Explorer & Filtered CSV Export (BUILD-13)
Author: Alisha Khan (Roll No. 2503201450012)
Project: Customer Rating & Review Analysis (CRRA)
"""

import streamlit as st
import pandas as pd
import src.data_loader as data_loader
import src.ui as ui

if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = data_loader.load_analytics_data()

df = st.session_state["df_filtered"]

ui.render_tailwind_header(
    "Data Explorer & Analytical Export",
    "Itemized Review Inspection & Multi-Format Dataset Download (OQ-07, BR-12, US-14)",
    "Data Access Suite"
)

# Summary Banner
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Active Filtered Rows", f"{len(df):,}")
col_m2.metric("Total Schema Columns", f"{len(df.columns)}")
col_m3.metric("Verified Review Share", f"{(df['is_verified_purchase'] == 1).mean() * 100:.1f}%")
col_m4.metric("Avg Review Length", f"{df['review_length_words'].mean():.1f} words")

st.markdown("---")

# Download Button (TC-F-13)
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv_data,
    file_name="crra_filtered_data.csv",
    mime="text/csv",
    help="Export active filtered dataset (all 38 joined analytical columns) as UTF-8 CSV",
    use_container_width=True
)

st.markdown("### 🔍 Itemized Analytical Records Explorer")
st.caption("Search across review text, sort by ratings, or filter by specific columns:")

# Search filter
search_term = st.text_input("Quick Keyword Search (filters review text & product name):", "")
if search_term:
    search_mask = (
        df["review_text"].str.contains(search_term, case=False, na=False) |
        df["product_name"].str.contains(search_term, case=False, na=False)
    )
    display_df = df[search_mask]
else:
    display_df = df

st.dataframe(display_df, use_container_width=True, height=450)

# Statistical Summary Expander
with st.expander("📊 Numerical Column Descriptive Statistics", expanded=False):
    st.dataframe(df.describe().round(2), use_container_width=True)
