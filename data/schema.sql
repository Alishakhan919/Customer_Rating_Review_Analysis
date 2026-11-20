-- ====================================================================
-- CUSTOMER RATING & REVIEW ANALYSIS (CRRA) - SQLITE DDL SCHEMA
-- Target Database: data/app.db
-- Specification: Step 8 Database Design
-- Author: Alisha Khan (Roll No. 2503201450012)
-- ====================================================================

PRAGMA foreign_keys = ON;

-- --------------------------------------------------------------------
-- 1. Dimension: Categories (dim_categories)
-- Grain: One record per distinct product category
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    category_code TEXT NOT NULL UNIQUE,
    target_benchmark_rating REAL NOT NULL DEFAULT 4.0 CHECK (target_benchmark_rating >= 1.0 AND target_benchmark_rating <= 5.0),
    created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

-- --------------------------------------------------------------------
-- 2. Dimension: Vendors / Suppliers (dim_vendors)
-- Grain: One record per third-party marketplace merchant
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_vendors (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_uid TEXT NOT NULL UNIQUE,
    vendor_name TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    sla_compliance_status TEXT NOT NULL DEFAULT 'Compliant' CHECK (sla_compliance_status IN ('Compliant', 'Non-Compliant', 'Under Review')),
    onboarding_date TEXT NOT NULL
);

-- --------------------------------------------------------------------
-- 3. Dimension: Products / SKUs (dim_products)
-- Grain: One record per individual product SKU
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    vendor_id INTEGER NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    product_cost REAL NOT NULL CHECK (product_cost > 0),
    launch_date TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (category_id) REFERENCES dim_categories (category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (vendor_id) REFERENCES dim_vendors (vendor_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- --------------------------------------------------------------------
-- 4. Dimension: Customers (dim_customers)
-- Grain: One record per customer profile
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_uid TEXT NOT NULL UNIQUE,
    customer_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 90),
    age_group TEXT NOT NULL CHECK (age_group IN ('18-25', '26-35', '36-50', '51+')),
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Non-Binary', 'Other')),
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    region TEXT NOT NULL CHECK (region IN ('North', 'South', 'East', 'West', 'Central')),
    signup_date TEXT NOT NULL
);

-- --------------------------------------------------------------------
-- 5. Fact Table: Customer Reviews (fact_reviews)
-- Grain: One record per submitted customer review event
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_uid TEXT NOT NULL UNIQUE,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_title TEXT,
    review_text TEXT NOT NULL,
    review_timestamp TEXT NOT NULL,
    review_date TEXT NOT NULL,
    review_year INTEGER NOT NULL,
    review_month INTEGER NOT NULL CHECK (review_month >= 1 AND review_month <= 12),
    review_day INTEGER NOT NULL CHECK (review_day >= 1 AND review_day <= 31),
    day_of_week TEXT NOT NULL CHECK (day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    hour_of_day INTEGER NOT NULL CHECK (hour_of_day >= 0 AND hour_of_day <= 23),
    is_verified_purchase INTEGER NOT NULL DEFAULT 1 CHECK (is_verified_purchase IN (0, 1)),
    helpful_votes INTEGER NOT NULL DEFAULT 0 CHECK (helpful_votes >= 0),
    review_length_words INTEGER NOT NULL CHECK (review_length_words >= 0),
    sentiment_score REAL NOT NULL CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0),
    sentiment_label TEXT NOT NULL CHECK (sentiment_label IN ('Positive', 'Neutral', 'Negative')),
    primary_defect_tag TEXT NOT NULL DEFAULT 'None' CHECK (primary_defect_tag IN ('None', 'Packaging', 'Sizing', 'Battery', 'Delivery', 'Build_Quality', 'Description_Mismatch')),
    return_intent_flag INTEGER NOT NULL DEFAULT 0 CHECK (return_intent_flag IN (0, 1)),
    rating_sentiment_divergence REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (product_id) REFERENCES dim_products (product_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES dim_customers (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- --------------------------------------------------------------------
-- Performance Indexes on Foreign Keys and Query Dimensions
-- --------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_reviews_product ON fact_reviews (product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_customer ON fact_reviews (customer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON fact_reviews (rating);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON fact_reviews (review_date);
CREATE INDEX IF NOT EXISTS idx_reviews_verified ON fact_reviews (is_verified_purchase);
CREATE INDEX IF NOT EXISTS idx_reviews_return ON fact_reviews (return_intent_flag);
CREATE INDEX IF NOT EXISTS idx_products_category ON dim_products (category_id);
CREATE INDEX IF NOT EXISTS idx_products_vendor ON dim_products (vendor_id);

-- --------------------------------------------------------------------
-- Unified Analytical Mart View (view_review_analytics)
-- Columns: 35 enriched business attributes for direct reporting
-- --------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS view_review_analytics AS
SELECT 
    r.review_id,
    r.review_uid,
    r.review_date,
    r.review_timestamp,
    r.review_year,
    r.review_month,
    r.day_of_week,
    r.hour_of_day,
    r.rating,
    CASE 
        WHEN r.rating = 5 THEN '5-Star (Delight)'
        WHEN r.rating = 4 THEN '4-Star (Satisfied)'
        WHEN r.rating = 3 THEN '3-Star (Neutral/Mixed)'
        WHEN r.rating = 2 THEN '2-Star (Dissatisfied)'
        ELSE '1-Star (Severe Defect)'
    END AS rating_tier,
    r.review_title,
    r.review_text,
    r.review_length_words,
    r.is_verified_purchase,
    r.helpful_votes,
    r.sentiment_score,
    r.sentiment_label,
    r.primary_defect_tag,
    r.return_intent_flag,
    r.rating_sentiment_divergence,
    p.product_id,
    p.sku,
    p.product_name,
    p.price,
    p.product_cost,
    c.category_id,
    c.category_name,
    c.target_benchmark_rating,
    v.vendor_id,
    v.vendor_name,
    v.state AS vendor_state,
    v.sla_compliance_status,
    cust.customer_id,
    cust.age,
    cust.age_group,
    cust.gender,
    cust.region AS customer_region,
    cust.state AS customer_state
FROM fact_reviews r
INNER JOIN dim_products p ON r.product_id = p.product_id
INNER JOIN dim_categories c ON p.category_id = c.category_id
INNER JOIN dim_vendors v ON p.vendor_id = v.vendor_id
INNER JOIN dim_customers cust ON r.customer_id = cust.customer_id;
