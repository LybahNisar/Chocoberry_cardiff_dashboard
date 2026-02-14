"""
HONEST VERIFICATION - Cross-check dashboard display vs raw data
"""

import pandas as pd
from pathlib import Path

print("=" * 80)
print("HONEST VERIFICATION: Dashboard Numbers vs Raw Data")
print("=" * 80)

# Load the CSV
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Clean revenue
if df['Revenue'].dtype == 'object':
    df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')
if df['Gross sales'].dtype == 'object':
    df['Gross sales'] = pd.to_numeric(df['Gross sales'].str.replace(',', ''), errors='coerce')

print("\n1. FULL DATE RANGE (Jan 4 - Feb 13):")
print("-" * 80)
print(f"Total Orders: {len(df)}")
print(f"Total Revenue: £{df['Revenue'].sum():,.2f}")
print(f"Total Gross Sales: £{df['Gross sales'].sum():,.2f}")
print(f"Average Order: £{df['Gross sales'].mean():.2f}")

# What the dashboard SHOULD show with full date range selected
print("\n2. WHAT DASHBOARD SHOWS (if full range selected):")
print("-" * 80)
print(f"Expected Total Orders: 6,523 (or 6,524 with header)")
print(f"Expected Revenue: £{df['Revenue'].sum()/1000:.1f}K")

# Check complete data (Jan 4 - Feb 12)
complete = df[df['Order time'].dt.date <= pd.to_datetime('2026-02-12').date()]
print("\n3. COMPLETE DATA ONLY (Jan 4 - Feb 12):")
print("-" * 80)
print(f"Total Orders: {len(complete)}")
print(f"Total Revenue: £{complete['Revenue'].sum():,.2f}")
print(f"Display: £{complete['Revenue'].sum()/1000:.1f}K")
print(f"Average Order: £{complete['Gross sales'].mean():.2f}")

# Verify top product
print("\n4. TOP PRODUCT VERIFICATION:")
print("-" * 80)
if 'Item' in df.columns:
    top_by_revenue = df.groupby('Item')['Revenue'].sum().sort_values(ascending=False).head(1)
    top_by_quantity = df.groupby('Item').size().sort_values(ascending=False).head(1)
    print(f"Top by Revenue: {top_by_revenue.index[0]} - £{top_by_revenue.values[0]:,.2f}")
    print(f"Top by Quantity: {top_by_quantity.index[0]} - {top_by_quantity.values[0]} items")
else:
    print("'Item' column not found - cannot verify top products")

# Verify weekly data
print("\n5. WEEKLY DATA VERIFICATION:")
print("-" * 80)
complete['Week'] = complete['Order time'].dt.to_period('W')
weekly = complete.groupby('Week').agg({
    'Revenue': 'sum',
    'Order ID': 'count'
})
print("Last 3 complete weeks:")
for week, row in weekly.tail(3).iterrows():
    print(f"  {week}: £{row['Revenue']:,.0f} ({row['Order ID']} orders)")

# Check for any data issues
print("\n6. DATA QUALITY CHECKS:")
print("-" * 80)
null_revenue = df['Revenue'].isna().sum()
null_items = df['Item'].isna().sum() if 'Item' in df.columns else 'N/A'
duplicates = df['Order ID'].duplicated().sum()

print(f"Null Revenue values: {null_revenue}")
print(f"Null Item values: {null_items}")
print(f"Duplicate Order IDs: {duplicates}")

if null_revenue > 0 or duplicates > 0:
    print("\n⚠️  WARNING: Data quality issues detected!")
else:
    print("\n✅ No data quality issues detected")

print("\n" + "=" * 80)
print("HONEST ASSESSMENT:")
print("=" * 80)
print("Compare these numbers with what you see on the dashboard.")
print("If they match, the dashboard is accurate.")
print("If they don't match, there's a calculation error.")
print("=" * 80)
