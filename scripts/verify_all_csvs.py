"""
COMPREHENSIVE CSV VERIFICATION
Checks EVERY CSV file and validates dashboard calculations
"""
import pandas as pd
from pathlib import Path
import sys

data_path = Path('data/raw/chocoberry_cardiff')

print("="*100)
print("COMPREHENSIVE DATA VERIFICATION - ALL CSV FILES")
print("="*100)

# List all CSV files
csv_files = list(data_path.glob('*.csv'))
print(f"\nFound {len(csv_files)} CSV files:")
for f in csv_files:
    print(f"  - {f.name}")

print("\n" + "="*100)
print("FILE 1: sales_data.csv - PRIMARY DATA SOURCE")
print("="*100)

# Load sales_data.csv
sales_df = pd.read_csv(data_path / 'sales_data.csv')
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'], errors='coerce')

# Convert numeric columns
numeric_cols = ['Gross sales', 'Revenue', 'Tax on gross sales', 'Delivery charges', 'Charges']
for col in numeric_cols:
    if col in sales_df.columns:
        sales_df[col] = pd.to_numeric(sales_df[col], errors='coerce').fillna(0)

# Filter valid dates only
sales_df = sales_df[sales_df['Order time'].notna()]

print(f"\nTotal valid transactions: {len(sales_df):,}")
print(f"Date range: {sales_df['Order time'].min()} to {sales_df['Order time'].max()}")

# Calculate KPIs
total_revenue = sales_df['Revenue'].sum()
total_gross = sales_df['Gross sales'].sum()
total_orders = len(sales_df)
avg_order = total_gross / total_orders
total_tax = sales_df['Tax on gross sales'].sum()
total_delivery = sales_df['Delivery charges'].sum()

print(f"\nKPI CALCULATIONS:")
print(f"  Total Revenue:      £{total_revenue:,.2f} (Display: £{total_revenue/1000:.1f}K)")
print(f"  Total Gross Sales:  £{total_gross:,.2f}")
print(f"  Average Order:      £{avg_order:.2f}")
print(f"  Total Orders:       {total_orders:,}")
print(f"  Total Tax:          £{total_tax:,.2f} (Display: £{total_tax/1000:.1f}K)")
print(f"  Delivery Charges:   £{total_delivery:.2f}")

# Peak hours
hourly = sales_df.groupby(sales_df['Order time'].dt.hour)['Gross sales'].sum().sort_values(ascending=False)
print(f"\nPEAK HOURS (Top 3):")
for idx, (hour, sales) in enumerate(hourly.head(3).items(), 1):
    print(f"  Peak #{idx}: {hour:02d}:00 - £{sales:,.2f}")

# Dispatch type breakdown
dispatch = sales_df.groupby('Dispatch type')['Gross sales'].sum()
dispatch_total = dispatch.sum()
print(f"\nDISPATCH TYPE BREAKDOWN:")
for dtype, sales in dispatch.sort_values(ascending=False).items():
    pct = (sales / dispatch_total * 100)
    print(f"  {dtype:15s}: £{sales:10,.2f} ({pct:5.1f}%)")

# Channel breakdown
channel = sales_df.groupby('Sales channel type')['Gross sales'].sum()
channel_total = channel.sum()
print(f"\nCHANNEL BREAKDOWN:")
for ch, sales in channel.sort_values(ascending=False).items():
    pct = (sales / channel_total * 100)
    print(f"  {ch:15s}: £{sales:10,.2f} ({pct:5.2f}%)")

print("\n" + "="*100)
print("CHECKING OTHER CSV FILES")
print("="*100)

# Check each CSV file
for csv_file in csv_files:
    if csv_file.name == 'sales_data.csv':
        continue
    
    print(f"\n{csv_file.name}:")
    try:
        df = pd.read_csv(csv_file)
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "="*100)
print("DASHBOARD EXPECTED VALUES")
print("="*100)
print(f"""
Based on sales_data.csv calculations:

KPI CARDS:
  Total Revenue:      £{total_revenue/1000:.1f}K
  Average Order:      £{avg_order:.2f}
  Total Orders:       {total_orders:,}
  Total Tax:          £{total_tax/1000:.1f}K
  Delivery Charges:   £{total_delivery:.2f}

PEAK HOURS:
  Peak #1: {hourly.index[0]:02d}:00 - £{hourly.iloc[0]:,.2f}
  Peak #2: {hourly.index[1]:02d}:00 - £{hourly.iloc[1]:,.2f}
  Peak #3: {hourly.index[2]:02d}:00 - £{hourly.iloc[2]:,.2f}
""")

print("="*100)
print("VERIFICATION COMPLETE")
print("="*100)
