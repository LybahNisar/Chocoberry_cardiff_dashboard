import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Check what happens on Feb 6
feb6_data = df[df['Order time'].dt.date == pd.to_datetime('2026-02-06').date()]
print(f"Orders on Feb 6 specifically: {len(feb6_data)}")
print(f"Last order time on Feb 6: {feb6_data['Order time'].max()}")

# My original filter
my_filter = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]
print(f"\nMy filter result: {len(my_filter)} orders")

# Dashboard-style filter (through END of Feb 6)
dashboard_filter = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] < '2026-02-07')]
print(f"Dashboard filter result: {len(dashboard_filter)} orders")

# Show the difference
print(f"\nDifference: {len(dashboard_filter) - len(my_filter)} orders")

# Also check total revenue
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
my_revenue = my_filter['Revenue'].sum()
dashboard_revenue = dashboard_filter['Revenue'].sum()

print(f"\nMy filter revenue: £{my_revenue:,.2f} (£{my_revenue/1000:.1f}K)")
print(f"Dashboard filter revenue: £{dashboard_revenue:,.2f} (£{dashboard_revenue/1000:.1f}K)")
