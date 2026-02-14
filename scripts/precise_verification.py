import pandas as pd

# Load CSV
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Clean numeric columns
for col in ['Revenue', 'Gross sales', 'Tax on gross sales', 'Delivery charges']:
    if df[col].dtype == 'object':
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

# Filter to match dashboard date range (Jan 4 - Feb 13)
start_date = pd.to_datetime('2026-01-04')
end_date = pd.to_datetime('2026-02-13')
filtered = df[(df['Order time'].dt.date >= start_date.date()) & 
              (df['Order time'].dt.date <= end_date.date())]

print("=" * 70)
print("PRECISE VERIFICATION - Dashboard vs CSV")
print("=" * 70)

print("\nDATE RANGE: 2026/01/04 - 2026/02/13")
print("-" * 70)

# KPI Metrics
total_orders = len(filtered)
total_revenue = filtered['Revenue'].sum()
avg_order = filtered['Gross sales'].mean()
total_tax = filtered['Tax on gross sales'].sum()
total_delivery = filtered['Delivery charges'].sum()

print(f"\n1. TOTAL ORDERS:")
print(f"   CSV: {total_orders}")
print(f"   Dashboard shows: 6,523")
print(f"   Match: {'YES' if total_orders == 6523 else 'NO - MISMATCH'}")

print(f"\n2. TOTAL REVENUE:")
print(f"   CSV: £{total_revenue:,.2f} = £{total_revenue/1000:.1f}K")
print(f"   Dashboard shows: £100.2K")
print(f"   Match: {'YES' if abs(total_revenue/1000 - 100.2) < 1 else 'NO - MISMATCH'}")

print(f"\n3. AVERAGE ORDER:")
print(f"   CSV: £{avg_order:.2f}")
print(f"   Dashboard shows: £14.75")
print(f"   Match: {'YES' if abs(avg_order - 14.75) < 1 else 'NO - MISMATCH'}")

print(f"\n4. TOTAL TAX:")
print(f"   CSV: £{total_tax:,.2f} = £{total_tax/1000:.1f}K")
print(f"   Dashboard shows: £3.7K")
print(f"   Match: {'YES' if abs(total_tax/1000 - 3.7) < 0.5 else 'NO - MISMATCH'}")

print(f"\n5. DELIVERY CHARGES:")
print(f"   CSV: £{total_delivery:,.2f}")
print(f"   Dashboard shows: £223.13")
print(f"   Match: {'YES' if abs(total_delivery - 223.13) < 10 else 'NO - MISMATCH'}")

# Weekly breakdown
print("\n" + "=" * 70)
print("WEEKLY BREAKDOWN VERIFICATION")
print("=" * 70)

filtered['Week'] = filtered['Order time'].dt.to_period('W')
weekly = filtered.groupby('Week').agg({
    'Revenue': 'sum',
    'Order ID': 'count'
}).reset_index()

print("\nWeek-by-week comparison:")
for idx, row in weekly.tail(5).iterrows():
    week_start = row['Week'].start_time.strftime('%b %d')
    print(f"Week of {week_start}: £{row['Revenue']:,.0f} ({row['Order ID']} orders)")

print("\n" + "=" * 70)
print("FINAL VERDICT")
print("=" * 70)

# Count matches
matches = 0
total_checks = 5

if total_orders == 6523: matches += 1
if abs(total_revenue/1000 - 100.2) < 1: matches += 1
if abs(avg_order - 14.75) < 1: matches += 1
if abs(total_tax/1000 - 3.7) < 0.5: matches += 1
if abs(total_delivery - 223.13) < 10: matches += 1

print(f"\nMatches: {matches}/{total_checks}")

if matches == total_checks:
    print("Status: ALL NUMBERS ACCURATE")
elif matches >= 4:
    print("Status: MOSTLY ACCURATE (minor differences)")
else:
    print("Status: SIGNIFICANT MISMATCHES FOUND")

print("=" * 70)
