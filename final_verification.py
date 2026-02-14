import pandas as pd
from pathlib import Path

# Load data
data_path = Path('data/raw/chocoberry_cardiff')
df = pd.read_csv(data_path / 'sales_data.csv')

# Convert columns EXACTLY as dashboard does
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Order time'] = pd.to_datetime(df['Order time'])

# Filter EXACTLY like dashboard (2026-01-04 to 2026-02-06)
filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]

# Calculate metrics EXACTLY as dashboard does
total_orders = len(filtered)
total_revenue = filtered['Revenue'].sum()  # Line 239 of dashboard
avg_order_value = filtered['Gross sales'].mean()  # Line 249 of dashboard

print("="*70)
print("FINAL DASHBOARD VERIFICATION - Using Correct Columns")
print("="*70)
print()
print("DASHBOARD SHOWS:")
print("  Total Revenue: £81.0K")
print("  Total Orders: 5,275")
print("  Average Order Value: £14.75")
print()
print("CSV CALCULATED VALUES:")
print(f"  Total Revenue: £{total_revenue/1000:.1f}K")
print(f"  Total Orders: {total_orders:,}")
print(f"  Average Order Value: £{avg_order_value:.2f}")
print()
print("="*70)
print("VERIFICATION RESULT:")
print("="*70)

all_match = True

if total_orders == 5275:
    print("✅ Total Orders: MATCH (5,275)")
else:
    print(f"❌ Total Orders: MISMATCH - CSV={total_orders}, Dashboard=5,275")
    all_match = False

revenue_k = total_revenue / 1000
if abs(revenue_k - 81.0) < 0.1:
    print(f"✅ Total Revenue: MATCH (£81.0K)")
else:
    print(f"❌ Total Revenue: MISMATCH - CSV=£{revenue_k:.1f}K, Dashboard=£81.0K")
    all_match = False

if abs(avg_order_value - 14.75) < 0.01:
    print(f"✅ Average Order Value: MATCH (£14.75)")
else:
    print(f"❌ Average Order Value: MISMATCH - CSV=£{avg_order_value:.2f}, Dashboard=£14.75")
    all_match = False

print()
if all_match:
    print("🎉 DASHBOARD IS 100% ACCURATE! 🎉")
else:
    print("⚠️  DISCREPANCIES FOUND - NEEDS INVESTIGATION")
print("="*70)
