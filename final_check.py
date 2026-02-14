import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)

# Dashboard-style filter (includes ALL of Feb 6)
correct_filter = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] < '2026-02-07')]

total_orders = len(correct_filter)
total_revenue = correct_filter['Revenue'].sum()
avg_order = correct_filter['Gross sales'].mean()

print("="*60)
print("CORRECT VERIFICATION (including full Feb 6)")
print("="*60)
print(f"Total Orders: {total_orders:,}")
print(f"Total Revenue: GBP{total_revenue/1000:.1f}K")
print(f"Average Order Value: GBP{avg_order:.2f}")
print()
print("DASHBOARD SHOWS:")
print("Total Orders: 5,275")
print("Total Revenue: GBP81.0K")
print("Average Order Value: GBP14.75")
print()
print("="*60)
if total_orders == 5275:
    print("MATCH! Dashboard is CORRECT!")
else:
    print(f"Still different: CSV={total_orders}, Dashboard=5275")
print("="*60)
