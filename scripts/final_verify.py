import pandas as pd
from pathlib import Path

# Load data exactly as dashboard does
data_path = Path('data/raw/chocoberry_cardiff')
df = pd.read_csv(data_path / 'sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Convert numeric columns
for col in ['Gross sales', 'Revenue', 'Tax on gross sales', 'Delivery charges']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Filter to date range shown in screenshot: 2026-01-04 to 2026-02-04
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-04')]

print("="*80)
print("FINAL VERIFICATION - Post Cache Clear")
print("="*80)
print(f"\nDate Range: Jan 04, 2026 - Feb 04, 2026")
print(f"Total Transactions: {len(df):,}")

# KPI Verification
total_revenue = df['Revenue'].sum()
total_gross = df['Gross sales'].sum()
total_orders = len(df)
avg_order = total_gross / total_orders
total_tax = df['Tax on gross sales'].sum()
total_delivery = df['Delivery charges'].sum()

print("\n" + "="*80)
print("KPI METRICS")
print("="*80)
print(f"Total Revenue:      £{total_revenue:,.2f}")
print(f"Total Gross Sales:  £{total_gross:,.2f}")
print(f"Average Order:      £{avg_order:.2f}")
print(f"Total Orders:       {total_orders:,}")
print(f"Total Tax:          £{total_tax:,.2f}")
print(f"Delivery Charges:   £{total_delivery:.2f}")

# Peak Hours Verification
print("\n" + "="*80)
print("PEAK HOURS")
print("="*80)
hourly = df.groupby(df['Order time'].dt.hour).agg({
    'Gross sales': 'sum',
    'Order ID': 'count'
})
hourly['Avg Order'] = hourly['Gross sales'] / hourly['Order ID']
hourly = hourly.sort_values('Gross sales', ascending=False)

for idx, (hour, row) in enumerate(hourly.head(3).iterrows(), 1):
    print(f"Peak #{idx}: Hour {hour:02d}:00 | £{row['Gross sales']:,.2f} | {int(row['Order ID'])} orders | Avg £{row['Avg Order']:.2f}")

print("\n" + "="*80)
print("DASHBOARD vs SOURCE COMPARISON")
print("="*80)

# Compare to screenshot values
print("\nScreenshot shows:")
print("  Total Revenue: £76,8xx (truncated)")
print("  Average Order: £14.77")
print("  Total Orders: 5,000")
print("  Peak #1 (21:00): £11,214")
print("  Peak #2 (20:00): £10,904")
print("  Peak #3 (22:00): £10,319")

print("\nSource data shows:")
print(f"  Total Revenue: £{total_revenue:,.2f}")
print(f"  Average Order: £{avg_order:.2f}")
print(f"  Total Orders: {total_orders:,}")
peak1 = hourly.iloc[0]
peak2 = hourly.iloc[1]
peak3 = hourly.iloc[2]
print(f"  Peak #1 (21:00): £{peak1['Gross sales']:,.2f}")
print(f"  Peak #2 (20:00): £{peak2['Gross sales']:,.2f}")
print(f"  Peak #3 (22:00): £{peak3['Gross sales']:,.2f}")

print("\n" + "="*80)
matches = []
if abs(avg_order - 14.77) < 0.01:
    matches.append("✅ Average Order MATCHES")
else:
    matches.append(f"❌ Average Order MISMATCH: Expected £14.77, Got £{avg_order:.2f}")

if total_orders == 5000:
    matches.append("✅ Total Orders MATCHES")
else:
    matches.append(f"❌ Total Orders MISMATCH: Expected 5000, Got {total_orders}")

if abs(peak1['Gross sales'] - 11214.22) < 1:
    matches.append("✅ Peak Hour #1 MATCHES")
else:
    matches.append(f"❌ Peak #1 MISMATCH")

if abs(peak2['Gross sales'] - 10903.53) < 1:
    matches.append("✅ Peak Hour #2 MATCHES")
else:
    matches.append(f"❌ Peak #2 MISMATCH")

if abs(peak3['Gross sales'] - 10318.79) < 1:
    matches.append("✅ Peak Hour #3 MATCHES")
else:
    matches.append(f"❌ Peak #3 MISMATCH")

for match in matches:
    print(match)

if all("✅" in m for m in matches):
    print("\n🎉 ALL VERIFIED VALUES MATCH! DASHBOARD IS ACCURATE!")
else:
    print("\n⚠️ SOME VALUES DO NOT MATCH")
print("="*80)
