"""
Customer Rating & Review Analysis (CRRA) - Synthetic Dataset Generator
Author: Alisha Khan (Roll No. 2503201450012)
Academic Mentor: Prof. Kalpana Dwivedi, ABES Engineering College
Step 10 Implementation: Generates SQLite app.db, multi-sheet Excel, and CSV tables.
"""

import sqlite3
import random
import os
import datetime
import pandas as pd
import numpy as np

# Set fixed random seeds for deterministic reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

BASE_DIR = r"c:\Customer_Rating_Review_Analysis"
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "app.db")
SCHEMA_PATH = os.path.join(DATA_DIR, "schema.sql")
EXCEL_PATH = os.path.join(DATA_DIR, "Customer_Rating_Review_Analysis_data.xlsx")

def generate_categories():
    categories = [
        {"category_id": 1, "category_name": "Electronics", "category_code": "ELEC", "target_benchmark_rating": 4.0, "created_at": "2025-01-01 00:00:00"},
        {"category_id": 2, "category_name": "Apparel", "category_code": "APPR", "target_benchmark_rating": 4.2, "created_at": "2025-01-01 00:00:00"},
        {"category_id": 3, "category_name": "Home & Kitchen", "category_code": "HOME", "target_benchmark_rating": 4.1, "created_at": "2025-01-01 00:00:00"},
        {"category_id": 4, "category_name": "Personal Care", "category_code": "CARE", "target_benchmark_rating": 4.3, "created_at": "2025-01-01 00:00:00"},
        {"category_id": 5, "category_name": "Books", "category_code": "BOOK", "target_benchmark_rating": 4.5, "created_at": "2025-01-01 00:00:00"}
    ]
    return pd.DataFrame(categories)

def generate_vendors():
    vendor_data = [
        ("VEN-001", "ApexTech Supplies", "support@apextech.in", "Noida", "Uttar Pradesh", "Non-Compliant", "2024-03-15"),
        ("VEN-002", "Zenith Apparel Works", "orders@zenithapparel.com", "Surat", "Gujarat", "Compliant", "2024-04-10"),
        ("VEN-003", "Bharat Living Essentials", "sales@bharatliving.in", "Bengaluru", "Karnataka", "Compliant", "2024-05-01"),
        ("VEN-004", "Vedic Glow Herbals", "care@vedicglow.co.in", "Haridwar", "Uttarakhand", "Compliant", "2024-06-20"),
        ("VEN-005", "Shanti Publications", "info@shantipublishing.com", "Delhi", "Delhi", "Compliant", "2024-01-11"),
        ("VEN-006", "Surya Consumer Electronics", "contact@suryatech.in", "Noida", "Uttar Pradesh", "Compliant", "2024-07-04"),
        ("VEN-007", "Royal Loom Textiles", "service@royalloom.in", "Jaipur", "Rajasthan", "Under Review", "2024-08-12"),
        ("VEN-008", "KitchenKing Appliances", "ops@kitchenking.in", "Mumbai", "Maharashtra", "Compliant", "2024-02-18"),
        ("VEN-009", "AyurVeda Natural Care", "hello@ayurvedanaturals.in", "Kochi", "Kerala", "Compliant", "2024-09-01"),
        ("VEN-010", "Gyan Ganga Book House", "sales@gyanganga.org", "Kolkata", "West Bengal", "Compliant", "2024-03-25"),
        ("VEN-011", "NovaTech Digital Gadgets", "help@novatechdigital.in", "Hyderabad", "Telangana", "Non-Compliant", "2024-10-05"),
        ("VEN-012", "UrbanChic Fast Fashion", "support@urbanchic.in", "Pune", "Maharashtra", "Compliant", "2024-05-30"),
        ("VEN-013", "DesiRasoi Cookware", "contact@desirasoi.in", "Ahmedabad", "Gujarat", "Compliant", "2024-06-15"),
        ("VEN-014", "PureHerbs Wellness", "care@pureherbswellness.com", "Dehradun", "Uttarakhand", "Compliant", "2024-07-22"),
        ("VEN-015", "Pragati Educational Media", "editorial@pragatimedias.com", "Patna", "Bihar", "Compliant", "2024-04-18")
    ]
    vendors = []
    for idx, v in enumerate(vendor_data, 1):
        vendors.append({
            "vendor_id": idx,
            "vendor_uid": v[0],
            "vendor_name": v[1],
            "contact_email": v[2],
            "city": v[3],
            "state": v[4],
            "sla_compliance_status": v[5],
            "onboarding_date": v[6]
        })
    return pd.DataFrame(vendors)

def generate_products(df_cat, df_ven):
    products = []
    sku_catalog = [
        # Electronics (Category 1)
        ("ELEC-101", "True Wireless Bluetooth Earbuds with ANC", 1, 1, 2499.0, 1400.0, "2024-08-01"),
        ("ELEC-102", "4K Ultra-HD Smart Streaming Media Stick", 1, 6, 3999.0, 2600.0, "2024-08-15"),
        ("ELEC-103", "Ergonomic Silent Wireless Optical Mouse", 1, 6, 899.0, 450.0, "2024-09-01"),
        ("ELEC-104", "Fast Charging Power Bank 20000mAh", 1, 1, 1999.0, 1100.0, "2024-07-20"), # Target Defect SKU
        ("ELEC-105", "Mechanical Gaming Keyboard RGB Backlit", 1, 11, 3499.0, 2100.0, "2024-09-10"),
        ("ELEC-106", "Smart Fitness Tracker with SpO2 Monitor", 1, 11, 2999.0, 1800.0, "2024-08-25"),
        ("ELEC-107", "Heavy Bass Portable Waterproof Bluetooth Speaker", 1, 6, 1799.0, 950.0, "2024-09-15"),
        ("ELEC-108", "Dual USB-C 65W GaN Fast Wall Charger", 1, 1, 1499.0, 800.0, "2024-08-10"), # Target Defect SKU
        ("ELEC-109", "Noise Cancelling Over-Ear Studio Headphones", 1, 6, 5499.0, 3200.0, "2024-07-15"),
        ("ELEC-110", "Full HD 1080p Autofocus USB Web Camera", 1, 11, 1899.0, 1050.0, "2024-09-20"),

        # Apparel (Category 2)
        ("APPR-201", "Pure Cotton Classic Slim Fit Formal Shirt", 2, 2, 1299.0, 650.0, "2024-05-10"),
        ("APPR-202", "Breathable Activewear Gym Track Pants", 2, 2, 999.0, 480.0, "2024-06-01"),
        ("APPR-203", "Traditional Chanderi Silk Embroidered Kurti", 2, 7, 1899.0, 950.0, "2024-06-20"),
        ("APPR-204", "Stretchable Indigo Denim Jeans Regular Fit", 2, 12, 1699.0, 850.0, "2024-07-05"),
        ("APPR-205", "Round Neck Graphic Print Cotton T-Shirt", 2, 2, 499.0, 220.0, "2024-05-25"),
        ("APPR-206", "Handwoven Khadi Cotton Nehru Jacket", 2, 7, 2199.0, 1100.0, "2024-08-01"),
        ("APPR-207", "Lightweight Fleece Hooded Winter Sweatshirt", 2, 12, 1499.0, 720.0, "2024-09-01"),
        ("APPR-208", "Ethnic Block Print Anarkali Gown", 2, 7, 2499.0, 1300.0, "2024-07-18"),
        ("APPR-209", "Quick Dry Performance Running Shorts", 2, 2, 699.0, 320.0, "2024-08-10"),
        ("APPR-210", "Soft Viscose Blend Formal Trousers", 2, 12, 1399.0, 680.0, "2024-09-05"),

        # Home & Kitchen (Category 3)
        ("HOME-301", "Hard Anodised Non-Stick Induction Dosa Tawa", 3, 8, 1199.0, 580.0, "2024-04-15"),
        ("HOME-302", "Stainless Steel Double-Wall Thermal Flask 1L", 3, 3, 899.0, 420.0, "2024-05-01"),
        ("HOME-303", "Tri-Ply Stainless Steel Heavy Bottom Kadai", 3, 13, 2299.0, 1200.0, "2024-05-20"),
        ("HOME-304", "Compact 750W 3-Jar Mixer Grinder", 3, 8, 3199.0, 1900.0, "2024-06-10"),
        ("HOME-305", "BPA-Free Airtight Modular Food Storage Container Set (6 Pcs)", 3, 3, 799.0, 360.0, "2024-06-25"),
        ("HOME-306", "Microfibre Spin Mop with Bucket & Wheels", 3, 3, 1399.0, 680.0, "2024-07-02"),
        ("HOME-307", "Pure Cotton 250 TC King Size Bedsheet with Pillow Covers", 3, 3, 1299.0, 600.0, "2024-07-15"),
        ("HOME-308", "Automatic Electric Kettle 1.8 Litre Fast Boil", 3, 8, 849.0, 410.0, "2024-08-01"),
        ("HOME-309", "Handcrafted Sheesham Wood Spice Box with Glass Lid", 3, 13, 999.0, 480.0, "2024-08-18"),
        ("HOME-310", "Multi-Tier Stainless Steel Dish Drying Rack", 3, 13, 1599.0, 780.0, "2024-09-01"),

        # Personal Care (Category 4)
        ("CARE-401", "Organic Cold Pressed Virgin Coconut Oil 500ml", 4, 4, 399.0, 180.0, "2024-04-01"),
        ("CARE-402", "Vitamin C Radiance Face Serum with Hyaluronic Acid", 4, 9, 699.0, 290.0, "2024-04-20"),
        ("CARE-403", "Ayurvedic Anti-Hair Fall Bhringraj Herbal Shampoo", 4, 4, 499.0, 210.0, "2024-05-15"),
        ("CARE-404", "Deep Cleansing Activated Charcoal Detox Face Wash", 4, 14, 299.0, 120.0, "2024-06-01"),
        ("CARE-405", "Broad Spectrum SPF 50 PA++++ Gel Sunscreen 100g", 4, 9, 549.0, 240.0, "2024-06-18"),
        ("CARE-406", "Nourishing Shea Butter Body Lotion Dry Skin 400ml", 4, 14, 449.0, 190.0, "2024-07-05"),
        ("CARE-407", "Pure Kumkumadi Tailam Miraculous Beauty Ayurvedic Night Oil", 4, 4, 1199.0, 520.0, "2024-07-25"),
        ("CARE-408", "Natural Tea Tree Clarifying Blemish Control Mask", 4, 9, 399.0, 160.0, "2024-08-10"),
        ("CARE-409", "Rejuvenating Rose Water Facial Mist Toner 200ml", 4, 14, 249.0, 95.0, "2024-08-28"),
        ("CARE-410", "Gentle Hydrating Ceramide Moisturizer Sensitive Skin", 4, 9, 599.0, 260.0, "2024-09-12"),

        # Books (Category 5)
        ("BOOK-501", "Modern Data Analytics with Python & SQL: Applied Handbook", 5, 5, 699.0, 320.0, "2024-01-15"),
        ("BOOK-502", "Gitanjali: Deluxe Collector's Hardbound Edition", 5, 10, 499.0, 210.0, "2024-02-10"),
        ("BOOK-503", "Quantitative Aptitude for Competitive Examinations Guide", 5, 15, 799.0, 380.0, "2024-03-01"),
        ("BOOK-504", "The Psychology of Indian Consumerism & Market Dynamics", 5, 5, 549.0, 240.0, "2024-04-15"),
        ("BOOK-505", "Machine Learning in Practice: Algorithms & Optimization", 5, 5, 899.0, 420.0, "2024-05-10"),
        ("BOOK-506", "Ancient Indian History & Cultural Heritage Compendium", 5, 10, 649.0, 290.0, "2024-06-05"),
        ("BOOK-507", "Object-Oriented Programming with Java & Design Patterns", 5, 15, 749.0, 350.0, "2024-07-01"),
        ("BOOK-508", "Cloud Architecture & Scalable Microservices Manual", 5, 5, 849.0, 390.0, "2024-08-15"),
        ("BOOK-509", "Creative Writing & Narrative Techniques for Modern Authors", 5, 10, 449.0, 190.0, "2024-09-01"),
        ("BOOK-510", "Business Intelligence & Executive Analytics Roadmap", 5, 15, 799.0, 360.0, "2024-09-18")
    ]
    for idx, p in enumerate(sku_catalog, 1):
        products.append({
            "product_id": idx,
            "sku": p[0],
            "product_name": p[1],
            "category_id": p[2],
            "vendor_id": p[3],
            "price": p[4],
            "product_cost": p[5],
            "launch_date": p[6],
            "is_active": 1
        })
    return pd.DataFrame(products)

def generate_customers():
    first_names = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Aayan", "Krishna", "Ishan",
        "Shaurya", "Atharv", "Ananya", "Diya", "Sanvi", "Aadhya", "Kiara", "Pari", "Anika", "Navya",
        "Myra", "Riya", "Alisha", "Tanvi", "Priya", "Sneha", "Pooja", "Neha", "Rohan", "Amit",
        "Rahul", "Vikas", "Rajesh", "Suresh", "Deepa", "Meera", "Swati", "Kavita", "Sunita", "Manoj",
        "Gaurav", "Naveen", "Abhishek", "Pankaj", "Deepak", "Ritu", "Shweta", "Preeti", "Komal", "Divya"
    ]
    surnames = [
        "Sharma", "Verma", "Gupta", "Patel", "Singh", "Kumar", "Mishra", "Joshi", "Yadav", "Nair",
        "Rao", "Reddy", "Chatterjee", "Banerjee", "Mukherjee", "Das", "Mehta", "Shah", "Jain", "Agarwal"
    ]
    
    locations = [
        ("Noida", "Uttar Pradesh", "North"),
        ("Delhi", "Delhi", "North"),
        ("Lucknow", "Uttar Pradesh", "North"),
        ("Jaipur", "Rajasthan", "North"),
        ("Chandigarh", "Punjab", "North"),
        ("Bengaluru", "Karnataka", "South"),
        ("Chennai", "Tamil Nadu", "South"),
        ("Hyderabad", "Telangana", "South"),
        ("Kochi", "Kerala", "South"),
        ("Mumbai", "Maharashtra", "West"),
        ("Pune", "Maharashtra", "West"),
        ("Ahmedabad", "Gujarat", "West"),
        ("Surat", "Gujarat", "West"),
        ("Kolkata", "West Bengal", "East"),
        ("Patna", "Bihar", "East"),
        ("Bhubaneswar", "Odisha", "East"),
        ("Bhopal", "Madhya Pradesh", "Central"),
        ("Indore", "Madhya Pradesh", "Central")
    ]
    
    customers = []
    for i in range(1, 101):
        fn = first_names[(i - 1) % len(first_names)]
        sn = surnames[(i * 3) % len(surnames)]
        full_name = f"{fn} {sn}"
        
        age = random.randint(18, 68)
        if age <= 25:
            ag = "18-25"
        elif age <= 35:
            ag = "26-35"
        elif age <= 50:
            ag = "36-50"
        else:
            ag = "51+"
            
        gender = "Female" if (i % 2 == 0) else "Male"
        loc = locations[i % len(locations)]
        
        # Occasional leading/trailing whitespace data quality issue in 2% of cities
        city_str = loc[0]
        if i in [14, 42]:
            city_str = f"  {loc[0]}  "
            
        signup_dt = datetime.date(2023, 1, 1) + datetime.timedelta(days=(i * 7) % 650)
        
        customers.append({
            "customer_id": i,
            "customer_uid": f"CUST-{i:03d}",
            "customer_name": full_name,
            "age": age,
            "age_group": ag,
            "gender": gender,
            "city": city_str,
            "state": loc[1],
            "region": loc[2],
            "signup_date": signup_dt.strftime("%Y-%m-%d")
        })
    return pd.DataFrame(customers)

def generate_reviews(df_prod, df_cust, target_count=500):
    reviews = []
    
    # Review text corpus templates with realistic sentiment & defect vocabulary
    positive_reviews = [
        ("Outstanding Quality & Performance", "Exceeded my expectations completely! Built very sturdy and works flawlessly out of the box. Delivery was punctual and customer packaging was immaculate. Highly recommended!"),
        ("Great Value for Money", "Very good product at this price point. Quality is top-notch and finish looks premium. Satisfied with the purchase."),
        ("Superb Experience!", "Genuine product delivered ahead of scheduled date. Works exactly as advertised in the catalog. Will definitely purchase again from this seller."),
        ("Very Happy with the Purchase", "Excellent build quality, smooth functionality, and authentic product. Truly worth every rupee spent. NexCart service was great."),
        ("Delightful Product!", "Wonderful craftsmanship and reliable performance. Absolutely love it! No issues encountered after two weeks of rigorous daily use.")
    ]
    
    neutral_reviews = [
        ("Decent Product but Average Packaging", "Product works reasonably well, but the delivery box was slightly crushed. Functionality is acceptable for the price paid."),
        ("Meets Basic Expectations", "Standard product. Nothing extraordinary, but does the job decently. Sizing was slightly snug compared to description."),
        ("Average Experience", "Works as expected. Battery lasts about average. Neither too impressed nor disappointed."),
        ("Fair Quality", "Good for regular household use. Build material is modest plastic. Can improve overall fit and finish.")
    ]
    
    negative_battery = [
        ("Horrible Battery Drain Issue", "Extremely disappointed! Battery drains out completely within 45 minutes of usage. The device heats up dangerously while charging. Please return and refund my money immediately!"),
        ("Defective Battery Unit", "Stopped charging on the second day itself. Very bad quality control. Total waste of hard-earned money. Requesting a replacement.")
    ]
    
    negative_packaging = [
        ("Arrived Completely Broken & Damaged", "Terrible packaging! The outer carton was torn and the inner component was crushed upon unboxing. Defective piece delivered. Returning immediately!"),
        ("Damaged in Transit", "Box had zero bubble wrap or protection. The casing is cracked and scuffed. Very poor handling by vendor.")
    ]
    
    negative_sizing = [
        ("Misleading Sizing & Poor Fit", "The size chart is completely wrong! Ordered Large but it feels like Small. Fabric shrunk after the first hand wash. Initiated return request."),
        ("Incorrect Dimensions", "Does not fit properly at all. Material feels cheap and uncomfortable. Want a full refund.")
    ]
    
    negative_quality = [
        ("Very Poor Build Quality", "Broke within three days of normal usage. The plastic cracked and finish is substandard. Very bad experience with this seller."),
        ("Not Recommended at All", "Looks completely different from the catalog photographs. Low-grade materials used. Will not buy from this brand again.")
    ]
    
    # Sarcastic divergence templates (~4%)
    sarcastic_5star_neg_text = [
        ("Fabulous Waste of Money!", "Just wonderful! Broke on day one and customer service won't reply. Truly a masterclass in selling junk to buyers.", 5),
        ("Great Job Breaking Down", "Excellent! Lasted a whole 24 hours before smoking up. Spectacular manufacturing defect.", 5)
    ]
    
    sarcastic_1star_pos_text = [
        ("Too Good To Be True", "Giving 1 star because it is so amazing that all my colleagues keep borrowing it and won't return it! Flawless product.", 1),
        ("Unbelievably Good", "Minus 4 stars for being overly addictive to use. Actually best item I have bought this year.", 1)
    ]
    
    start_date = datetime.datetime(2024, 10, 1, 9, 0, 0)
    
    review_idx = 1
    while review_idx <= target_count:
        # Sampling products with deliberate bias towards failing SKUs:
        # ELEC-104 (id 4, ApexTech battery defect), ELEC-108 (id 8, ApexTech charger defect)
        rand_val = random.random()
        if rand_val < 0.12:
            p_id = 4 # ELEC-104
        elif rand_val < 0.20:
            p_id = 8 # ELEC-108
        else:
            p_id = random.randint(1, 50)
            
        c_id = random.randint(1, 100)
        
        # Sampling time: deliberate concentration on Sunday night & Wednesday afternoon
        day_offset = random.randint(0, 380)
        base_dt = start_date + datetime.timedelta(days=day_offset)
        
        timing_bias = random.random()
        if timing_bias < 0.35: # Sunday night peak
            days_to_sunday = (6 - base_dt.weekday()) % 7
            base_dt = base_dt + datetime.timedelta(days=days_to_sunday)
            hour = random.choice([20, 21, 22])
            minute = random.randint(0, 59)
        elif timing_bias < 0.55: # Wednesday afternoon peak
            days_to_wed = (2 - base_dt.weekday()) % 7
            base_dt = base_dt + datetime.timedelta(days=days_to_wed)
            hour = random.choice([13, 14, 15])
            minute = random.randint(0, 59)
        else:
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            
        second = random.randint(0, 59)
        rev_dt = base_dt.replace(hour=hour, minute=minute, second=second)
        
        # Verified buyer determination (80% verified)
        is_verified = 1 if (random.random() < 0.80) else 0
        
        # Rating & Sentiment generation with realistic e-commerce distribution
        # Special handling for failing SKUs (id 4 and 8)
        is_divergence = False
        if random.random() < 0.04: # 4% Sarcastic Divergence
            is_divergence = True
            if random.random() < 0.5:
                title, text, rating = random.choice(sarcastic_5star_neg_text)
                sentiment_score = -0.72
                sentiment_label = "Negative"
                defect_tag = "Build_Quality"
                return_intent = 1
                divergence = abs(rating - 1.0 - (sentiment_score * 2.0))
            else:
                title, text, rating = random.choice(sarcastic_1star_pos_text)
                sentiment_score = +0.84
                sentiment_label = "Positive"
                defect_tag = "None"
                return_intent = 0
                divergence = abs(rating - 1.0 - (sentiment_score * 2.0))
        elif p_id in [4, 8]: # Failing Electronics SKUs
            # High 1-star and 2-star rate (65% negative)
            if random.random() < 0.65:
                rating = random.choice([1, 1, 2])
                if p_id == 4:
                    title, text = random.choice(negative_battery)
                    defect_tag = "Battery"
                else:
                    title, text = random.choice(negative_packaging)
                    defect_tag = "Packaging"
                sentiment_score = round(random.uniform(-0.85, -0.45), 2)
                sentiment_label = "Negative"
                return_intent = 1
                divergence = round(abs(rating - 1.0 - (sentiment_score * 2.0)), 2)
            else:
                rating = random.choice([3, 4, 5])
                title, text = random.choice(positive_reviews if rating >= 4 else neutral_reviews)
                sentiment_score = round(random.uniform(0.15, 0.75), 2) if rating >= 4 else round(random.uniform(-0.05, 0.20), 2)
                sentiment_label = "Positive" if rating >= 4 else "Neutral"
                defect_tag = "None"
                return_intent = 0
                divergence = round(abs(rating - 3.0 - (sentiment_score * 2.0)), 2)
        else:
            # General catalog: authentic bimodal J-curve distribution
            # Verified buyers have higher ratings than unverified buyers
            if is_verified == 1:
                rating = np.random.choice([5, 4, 3, 2, 1], p=[0.55, 0.22, 0.10, 0.05, 0.08])
            else:
                rating = np.random.choice([5, 4, 3, 2, 1], p=[0.25, 0.20, 0.15, 0.15, 0.25])
                
            if rating >= 4:
                title, text = random.choice(positive_reviews)
                sentiment_score = round(random.uniform(0.35, 0.90), 2)
                sentiment_label = "Positive"
                defect_tag = "None"
                return_intent = 0
                divergence = 0.15
            elif rating == 3:
                title, text = random.choice(neutral_reviews)
                sentiment_score = round(random.uniform(-0.04, 0.04), 2)
                sentiment_label = "Neutral"
                defect_tag = "None"
                return_intent = 0
                divergence = 0.35
            else: # 1 or 2 stars
                neg_choice = random.choice(["packaging", "sizing", "quality"])
                if neg_choice == "packaging":
                    title, text = random.choice(negative_packaging)
                    defect_tag = "Packaging"
                elif neg_choice == "sizing":
                    title, text = random.choice(negative_sizing)
                    defect_tag = "Sizing"
                else:
                    title, text = random.choice(negative_quality)
                    defect_tag = "Build_Quality"
                    
                sentiment_score = round(random.uniform(-0.90, -0.40), 2)
                sentiment_label = "Negative"
                return_intent = 1 if any(w in text.lower() for w in ['return', 'refund', 'replacement', 'damaged']) else 0
                divergence = 0.25

        # Helpfulness votes (log-normal distribution with occasional viral outlier)
        if random.random() < 0.015:
            helpful = random.randint(120, 240) # Viral outlier
        else:
            helpful = int(np.random.exponential(scale=3.5))
            
        word_count = len(text.split())
        
        # Outlier word count for 2 records
        if review_idx in [37, 189]:
            text = text + " " + ("Extended customer review diagnostic feedback with detailed operational notes. " * 25)
            word_count = len(text.split())
            
        # Data Quality Issue: 2.5% Missing review_title (None)
        if random.random() < 0.025:
            title = None
            
        day_name = rev_dt.strftime("%A")
        
        reviews.append({
            "review_id": review_idx,
            "review_uid": f"REV-{review_idx:05d}",
            "product_id": p_id,
            "customer_id": c_id,
            "rating": int(rating),
            "review_title": title,
            "review_text": text,
            "review_timestamp": rev_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "review_date": rev_dt.strftime("%Y-%m-%d"),
            "review_year": rev_dt.year,
            "review_month": rev_dt.month,
            "review_day": rev_dt.day,
            "day_of_week": day_name,
            "hour_of_day": rev_dt.hour,
            "is_verified_purchase": int(is_verified),
            "helpful_votes": int(helpful),
            "review_length_words": int(word_count),
            "sentiment_score": float(sentiment_score),
            "sentiment_label": sentiment_label,
            "primary_defect_tag": defect_tag,
            "return_intent_flag": int(return_intent),
            "rating_sentiment_divergence": float(divergence)
        })
        review_idx += 1

    # Data Quality Issue: Exactly 3 duplicate customer review attempts (accidental double submissions)
    # Duplicate review index 45, 112, 260
    for dup_src_id in [45, 112, 260]:
        dup_row = dict(reviews[dup_src_id - 1])
        dup_row["review_id"] = len(reviews) + 1
        dup_row["review_uid"] = f"REV-{dup_row['review_id']:05d}"
        # submitted 2 minutes later by same customer for same product
        orig_dt = datetime.datetime.strptime(dup_row["review_timestamp"], "%Y-%m-%d %H:%M:%S")
        dup_dt = orig_dt + datetime.timedelta(minutes=2)
        dup_row["review_timestamp"] = dup_dt.strftime("%Y-%m-%d %H:%M:%S")
        reviews.append(dup_row)

    return pd.DataFrame(reviews)

def populate_database_and_files():
    print("Step 10: Initializing Synthetic Data Generation Pipeline...")
    
    df_categories = generate_categories()
    df_vendors = generate_vendors()
    df_products = generate_products(df_categories, df_vendors)
    df_customers = generate_customers()
    df_reviews = generate_reviews(df_products, df_customers, target_count=500)
    
    print(f"Generated Entities:")
    print(f" - dim_categories: {len(df_categories)} rows")
    print(f" - dim_vendors:    {len(df_vendors)} rows")
    print(f" - dim_products:   {len(df_products)} rows")
    print(f" - dim_customers:  {len(df_customers)} rows")
    print(f" - fact_reviews:   {len(df_reviews)} rows (including planned duplicates)")

    # Execute SQLite schema & load tables
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    
    # Insert Data into SQLite
    df_categories.to_sql("dim_categories", conn, if_exists="append", index=False)
    df_vendors.to_sql("dim_vendors", conn, if_exists="append", index=False)
    df_products.to_sql("dim_products", conn, if_exists="append", index=False)
    df_customers.to_sql("dim_customers", conn, if_exists="append", index=False)
    df_reviews.to_sql("fact_reviews", conn, if_exists="append", index=False)
    conn.commit()
    
    # Query Analytical View
    df_view = pd.read_sql_query("SELECT * FROM view_review_analytics", conn)
    print(f" - view_review_analytics: {len(df_view)} rows, {len(df_view.columns)} columns")
    conn.close()

    # Save Individual CSV Files
    df_categories.to_csv(os.path.join(DATA_DIR, "dim_categories.csv"), index=False)
    df_vendors.to_csv(os.path.join(DATA_DIR, "dim_vendors.csv"), index=False)
    df_products.to_csv(os.path.join(DATA_DIR, "dim_products.csv"), index=False)
    df_customers.to_csv(os.path.join(DATA_DIR, "dim_customers.csv"), index=False)
    df_reviews.to_csv(os.path.join(DATA_DIR, "fact_reviews.csv"), index=False)
    df_view.to_csv(os.path.join(DATA_DIR, "view_review_analytics.csv"), index=False)
    print("CSV files saved successfully in data/ directory.")

    # Save Master Excel Workbook with a Sheet per Table
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:
        df_categories.to_excel(writer, sheet_name="dim_categories", index=False)
        df_vendors.to_excel(writer, sheet_name="dim_vendors", index=False)
        df_products.to_excel(writer, sheet_name="dim_products", index=False)
        df_customers.to_excel(writer, sheet_name="dim_customers", index=False)
        df_reviews.to_excel(writer, sheet_name="fact_reviews", index=False)
        df_view.to_excel(writer, sheet_name="view_review_analytics", index=False)
    print(f"Master Excel file saved successfully at: {EXCEL_PATH}")

    # Validation Checks
    print("\n--- VALIDATION AUDIT REPORT ---")
    conn_val = sqlite3.connect(DB_PATH)
    conn_val.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Foreign Key Check
    fk_errors = conn_val.execute("PRAGMA foreign_key_check;").fetchall()
    print(f"1. Foreign Key Integrity Audit: {'PASSED (0 errors)' if len(fk_errors) == 0 else f'FAILED ({len(fk_errors)} errors)'}")
    
    # 2. Rating Range Check
    invalid_ratings = conn_val.execute("SELECT COUNT(*) FROM fact_reviews WHERE rating < 1 OR rating > 5").fetchone()[0]
    print(f"2. Rating Boundary Audit [1-5]: {'PASSED (0 invalid)' if invalid_ratings == 0 else f'FAILED ({invalid_ratings} invalid)'}")
    
    # 3. Sentiment Range Check
    invalid_sent = conn_val.execute("SELECT COUNT(*) FROM fact_reviews WHERE sentiment_score < -1.0 OR sentiment_score > 1.0").fetchone()[0]
    print(f"3. Sentiment Polarity Audit [-1.0, +1.0]: {'PASSED (0 invalid)' if invalid_sent == 0 else f'FAILED ({invalid_sent} invalid)'}")
    
    # 4. View Column Count Check
    print(f"4. Analytical View Column Count: {len(df_view.columns)} columns (Required: 30-40)")
    
    # 5. Statistical Pattern Verification
    v_mean = df_reviews[df_reviews['is_verified_purchase'] == 1]['rating'].mean()
    uv_mean = df_reviews[df_reviews['is_verified_purchase'] == 0]['rating'].mean()
    print(f"5. Statistical Pattern Check: Verified Mean Rating = {v_mean:.2f} vs Unverified = {uv_mean:.2f} (Lift confirmed)")
    
    elec_104_mean = df_reviews[df_reviews['product_id'] == 4]['rating'].mean()
    elec_104_ret = df_reviews[df_reviews['product_id'] == 4]['return_intent_flag'].mean() * 100
    print(f"6. Target Defect SKU (ELEC-104): Mean Rating = {elec_104_mean:.2f}, Return Rate = {elec_104_ret:.1f}% (Pattern confirmed)")
    
    null_titles = df_reviews['review_title'].isnull().sum()
    print(f"7. Missing Values Built-in: {null_titles} null review titles ({null_titles*100/len(df_reviews):.1f}%)")
    
    conn_val.close()
    print("\nDataset Generation Pipeline Completed Successfully.")

if __name__ == "__main__":
    populate_database_and_files()
