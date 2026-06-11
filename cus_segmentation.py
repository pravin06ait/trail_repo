# ============================================
# CUSTOMER SEGMENTATION USING RFM ANALYSIS
# ============================================

import pandas as pd
import numpy as np

# ============================================
# LOAD CLEANED DATASET
# ============================================

df = pd.read_csv("cleaned_online_retail.csv")

# ============================================
# CONVERT DATE COLUMN
# ============================================

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# ============================================
# CREATE TOTAL PRICE COLUMN
# ============================================

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# ============================================
# CREATE REFERENCE DATE
# (1 day after latest purchase)
# ============================================

reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# ============================================
# CREATE RFM TABLE
# ============================================

rfm = df.groupby('CustomerID').agg(

    Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),

    Frequency=('InvoiceNo', 'nunique'),

    Monetary=('TotalPrice', 'sum')

)

# ============================================
# RESET INDEX
# ============================================

rfm = rfm.reset_index()

# ============================================
# CREATE RFM SCORES
# USING QUANTILES
# ============================================

# Recency Score
rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    4,
    labels=[4,3,2,1]
)

# Frequency Score
rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    4,
    labels=[1,2,3,4]
)

# Monetary Score
rfm['M_Score'] = pd.qcut(
    rfm['Monetary'],
    4,
    labels=[1,2,3,4]
)

# ============================================
# COMBINE RFM SCORES
# ============================================

rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

# ============================================
# CUSTOMER SEGMENTATION LOGIC
# ============================================

def customer_segment(row):

    r = int(row['R_Score'])
    f = int(row['F_Score'])
    m = int(row['M_Score'])

    # Champions
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'

    # Loyal Customers
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'

    # Big Spenders
    elif m >= 4:
        return 'Big Spenders'

    # At Risk
    elif r <= 2 and f >= 3:
        return 'At Risk'

    # Lost Customers
    elif r == 1 and f == 1:
        return 'Lost Customers'

    else:
        return 'Regular Customers'

# Apply segmentation
rfm['Customer_Segment'] = rfm.apply(customer_segment, axis=1)

# ============================================
# DISPLAY RESULTS
# ============================================

print("\nRFM TABLE:\n")
print(rfm.head())

# ============================================
# SEGMENT COUNTS
# ============================================

print("\nCUSTOMER SEGMENT COUNTS:\n")
print(rfm['Customer_Segment'].value_counts())

# ============================================
# SAVE OUTPUT
# ============================================

rfm.to_csv("customer_rfm_segmentation.csv", index=False)

print("\nRFM segmentation file saved successfully!")
print("Successfully completed customer segmentation using RFM analysis.")
print("RFM segmentation process completed without errors.")
print("Customer segmentation using RFM analysis executed successfully.")
print("RFM segmentation completed successfully. Output saved to 'customer_rfm_segmentation.csv'.")