import pandas as pd

# Load CSV
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Clean revenue
if df['Revenue'].dtype == 'object':
    df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')

print("=" * 60)
print("HONEST DATA VERIFICATION")
print("=" * 60)

print(f"\n1. TOTAL DATA:")
print(f"   Rows: {len(df)}")
print(f"   Date Range: {df['Order time'].min().date()} to {df['Order time'].max().date()}")
print(f"   Total Revenue: £{df['Revenue'].sum():,.2f}")

print(f"\n2. COMPLETE DATA (Jan 4 - Feb 12):")
complete = df[df['Order time'].dt.date <= pd.to_datetime('2026-02-12').date()]
print(f"   Rows: {len(complete)}")
print(f"   Revenue: £{complete['Revenue'].sum():,.2f}")

print(f"\n3. WHAT DASHBOARD SHOULD SHOW:")
print(f"   If full range selected: £{df['Revenue'].sum()/1000:.1f}K")
print(f"   If Jan 4-Feb 12 selected: £{complete['Revenue'].sum()/1000:.1f}K")

print(f"\n4. YOUR SCREENSHOT SHOWS:")
print(f"   £100.2K")

print(f"\n5. VERDICT:")
dashboard_value = 100.2
actual_value = complete['Revenue'].sum() / 1000

if abs(dashboard_value - actual_value) < 5:
    print(f"   ✅ DASHBOARD IS ACCURATE")
    print(f"   Dashboard: £{dashboard_value}K")
    print(f"   Actual: £{actual_value:.1f}K")
    print(f"   Difference: £{abs(dashboard_value - actual_value):.1f}K (acceptable)")
else:
    print(f"   ❌ DASHBOARD MISMATCH")
    print(f"   Dashboard: £{dashboard_value}K")
    print(f"   Actual: £{actual_value:.1f}K")
    print(f"   Difference: £{abs(dashboard_value - actual_value):.1f}K")

print("=" * 60)
