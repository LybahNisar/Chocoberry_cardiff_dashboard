import pandas as pd

# Load CSV
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Clean revenue
if df['Revenue'].dtype == 'object':
    df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')

# Filter to date range (Jan 4 - Feb 13)
filtered = df[(df['Order time'].dt.date >= pd.to_datetime('2026-01-04').date()) & 
              (df['Order time'].dt.date <= pd.to_datetime('2026-02-13').date())]

print("=" * 70)
print("WEEKLY TRADING PATTERN VERIFICATION")
print("=" * 70)

# Get day of week
filtered['DayOfWeek'] = filtered['Order time'].dt.day_name()

# Group by day of week
day_summary = filtered.groupby('DayOfWeek').agg({
    'Revenue': 'sum',
    'Order ID': 'count'
}).reset_index()

# Sort by day order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_summary['DayOfWeek'] = pd.Categorical(day_summary['DayOfWeek'], categories=day_order, ordered=True)
day_summary = day_summary.sort_values('DayOfWeek')

print("\nRevenue by Day of Week:")
print("-" * 70)
for idx, row in day_summary.iterrows():
    print(f"{row['DayOfWeek']:12} £{row['Revenue']:>10,.2f} ({row['Order ID']:>4} orders)")

print("\n" + "=" * 70)
print("DASHBOARD COMPARISON:")
print("=" * 70)
print("Dashboard shows:")
print("  Busiest Day: Sunday - £17,357 (1099 Orders)")
print("  Slowest Day: Monday - £12,081 (788 Orders)")

print("\nActual from CSV:")
busiest = day_summary.loc[day_summary['Revenue'].idxmax()]
slowest = day_summary.loc[day_summary['Revenue'].idxmin()]
print(f"  Busiest Day: {busiest['DayOfWeek']} - £{busiest['Revenue']:,.0f} ({busiest['Order ID']:.0f} Orders)")
print(f"  Slowest Day: {slowest['DayOfWeek']} - £{slowest['Revenue']:,.0f} ({slowest['Order ID']:.0f} Orders)")

print("\n" + "=" * 70)
if abs(busiest['Revenue'] - 17357) < 100 and abs(slowest['Revenue'] - 12081) < 100:
    print("VERDICT: Dashboard numbers are ACCURATE")
else:
    print("VERDICT: Dashboard numbers DO NOT MATCH")
print("=" * 70)
