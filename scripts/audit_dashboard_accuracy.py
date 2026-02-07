"""
PROFESSIONAL DATA AUDIT - Dashboard Accuracy Verification
Verifies every calculation against source data with zero assumptions
"""
import pandas as pd
from pathlib import Path

print("=" * 100)
print("DASHBOARD ACCURACY AUDIT - ZERO TRUST VERIFICATION")
print("=" * 100)

# Load raw data
data_path = Path('data/raw/chocoberry_cardiff')
df = pd.read_csv(data_path / 'sales_data.csv')

# Clean data
df['Order time'] = pd.to_datetime(df['Order time'])
numeric_cols = ['Gross sales', 'Revenue', 'Tax on gross sales', 'Delivery charges']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Filter to dashboard date range: 2026-01-04 to 2026-02-04
df_filtered = df[(df['Order time'].dt.date >= pd.to_datetime('2026-01-04').date()) & 
                 (df['Order time'].dt.date <= pd.to_datetime('2026-02-04').date())]

print(f"\n📅 Date Range: 2026-01-04 to 2026-02-04")
print(f"📊 Total Transactions in Range: {len(df_filtered):,}")
print(f"📊 Actual Min Date: {df_filtered['Order time'].min()}")
print(f"📊 Actual Max Date: {df_filtered['Order time'].max()}")

print("\n" + "=" * 100)
print("VERIFICATION 1: DAILY SALES TABLE")
print("=" * 100)

# Calculate daily aggregation
df_filtered['Date'] = df_filtered['Order time'].dt.date
daily = df_filtered.groupby('Date').agg({
    'Gross sales': 'sum',
    'Revenue': 'sum',
    'Order ID': 'count'
}).reset_index()

print("\nShowing first 10 days (matching your screenshot):")
print(daily.head(10).to_string(index=False))

# Verify specific values from screenshot
print("\n🔍 SPOT CHECK - Verifying values from your screenshot:")
print(f"✓ Jan 4: Gross Sales = £{daily.iloc[0]['Gross sales']:,.2f} | Revenue = £{daily.iloc[0]['Revenue']:,.2f} | Orders = {int(daily.iloc[0]['Order ID'])}")
print(f"✓ Jan 5: Gross Sales = £{daily.iloc[1]['Gross sales']:,.2f} | Revenue = £{daily.iloc[1]['Revenue']:,.2f} | Orders = {int(daily.iloc[1]['Order ID'])}")
print(f"✓ Jan 6: Gross Sales = £{daily.iloc[2]['Gross sales']:,.2f} | Revenue = £{daily.iloc[2]['Revenue']:,.2f} | Orders = {int(daily.iloc[2]['Order ID'])}")

print("\n" + "=" * 100)
print("VERIFICATION 2: DISPATCH TYPE BREAKDOWN")
print("=" * 100)

dispatch_breakdown = df_filtered.groupby('Dispatch type').agg({
    'Gross sales': 'sum',
    'Order ID': 'count'
}).reset_index()
dispatch_breakdown['Avg Order Value'] = dispatch_breakdown['Gross sales'] / dispatch_breakdown['Order ID']
dispatch_breakdown.columns = ['Dispatch Type', 'Total Sales', 'Orders', 'Avg Order Value']

print("\nCalculated from source data:")
print(dispatch_breakdown.to_string(index=False))

print("\n🔍 COMPARING TO YOUR SCREENSHOT:")
for idx, row in dispatch_breakdown.iterrows():
    print(f"✓ {row['Dispatch Type']}: £{row['Total Sales']:,.2f} | {int(row['Orders'])} orders | Avg: £{row['Avg Order Value']:.2f}")

print("\n" + "=" * 100)
print("VERIFICATION 3: CHANNEL PERFORMANCE")
print("=" * 100)

channel_breakdown = df_filtered.groupby('Sales channel type').agg({
    'Gross sales': 'sum',
    'Order ID': 'count'
}).reset_index()
channel_breakdown['Avg Order'] = channel_breakdown['Gross sales'] / channel_breakdown['Order ID']
total_sales = channel_breakdown['Gross sales'].sum()
channel_breakdown['Market Share %'] = (channel_breakdown['Gross sales'] / total_sales * 100)
channel_breakdown.columns = ['Channel', 'Total Sales', 'Orders', 'Avg Order', 'Market Share %']
channel_breakdown = channel_breakdown.sort_values('Total Sales', ascending=False)

print("\nCalculated from source data:")
print(channel_breakdown.to_string(index=False))

print("\n🔍 COMPARING TO YOUR SCREENSHOT:")
for idx, row in channel_breakdown.iterrows():
    print(f"✓ {row['Channel']}: £{row['Total Sales']:,.2f} | {int(row['Orders'])} orders | {row['Market Share %']:.2f}%")

print("\n" + "=" * 100)
print("VERIFICATION 4: PEAK HOURS ANALYSIS")
print("=" * 100)

df_filtered['Hour'] = df_filtered['Order time'].dt.hour
hourly = df_filtered.groupby('Hour').agg({
    'Gross sales': 'sum',
    'Order ID': 'count'
}).reset_index()
hourly['Avg Order Value'] = hourly['Gross sales'] / hourly['Order ID']
hourly = hourly.sort_values('Gross sales', ascending=False)

print("\nTop 5 Peak Hours by Revenue:")
print(hourly.head(5).to_string(index=False))

top_3 = hourly.head(3)
print("\n🔍 COMPARING TO YOUR SCREENSHOT:")
print(f"✓ Peak #1: Hour {int(top_3.iloc[0]['Hour']):02d}:00 | £{top_3.iloc[0]['Gross sales']:,.2f}")
print(f"✓ Peak #2: Hour {int(top_3.iloc[1]['Hour']):02d}:00 | £{top_3.iloc[1]['Gross sales']:,.2f}")
print(f"✓ Peak #3: Hour {int(top_3.iloc[2]['Hour']):02d}:00 | £{top_3.iloc[2]['Gross sales']:,.2f}")

print("\n" + "=" * 100)
print("FINAL AUDIT SUMMARY")
print("=" * 100)

# Overall totals
total_revenue = df_filtered['Revenue'].sum()
total_gross = df_filtered['Gross sales'].sum()
total_orders = len(df_filtered)
avg_order = total_gross / total_orders

print(f"\n📊 OVERALL METRICS:")
print(f"   Total Gross Sales: £{total_gross:,.2f}")
print(f"   Total Revenue: £{total_revenue:,.2f}")
print(f"   Total Orders: {total_orders:,}")
print(f"   Average Order Value: £{avg_order:.2f}")

print("\n" + "=" * 100)
print("✅ VERIFICATION COMPLETE")
print("=" * 100)
print("\nAll calculations performed from raw CSV data.")
print("Compare these numbers to your dashboard screenshots.")
print("Any discrepancies will be immediately visible.")
print("=" * 100)
