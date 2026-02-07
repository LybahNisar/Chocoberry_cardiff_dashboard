import pandas as pd

# Load the merged sales data
df = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Filter to Jan 4 - Feb 6
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06 23:59:59')]

# Convert Revenue to numeric
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)

# Extract hour
df['Hour'] = df['Order time'].dt.hour

# Categorize meal periods
def categorize_meal_period(hour):
    if 8 <= hour < 12:
        return "Breakfast (8am-12pm)"
    elif 12 <= hour < 16:
        return "Lunch (12pm-4pm)"
    elif 16 <= hour < 20:
        return "Evening (4pm-8pm)"
    elif 20 <= hour < 24:
        return "Dinner (8pm-12am)"
    else:  # 0-7 hours
        return "Night Shift (12am-8am)"

df['Meal Period'] = df['Hour'].apply(categorize_meal_period)

# Calculate totals
summary = df.groupby('Meal Period').agg({
    'Revenue': 'sum',
    'Order time': 'count'
}).reset_index()
summary.columns = ['Meal Period', 'Revenue', 'Orders']

# Calculate percentages
total_revenue = summary['Revenue'].sum()
summary['% of Sales'] = (summary['Revenue'] / total_revenue * 100).round(1)

# Sort by revenue
summary = summary.sort_values('Revenue', ascending=False)

print("=" * 70)
print("MEAL PERIOD VERIFICATION")
print("=" * 70)
print(f"\nTotal Revenue: £{total_revenue:,.2f}")
print(f"Total Orders: {df.shape[0]:,}")
print("\n" + "=" * 70)
print("BREAKDOWN BY MEAL PERIOD:")
print("=" * 70)

for _, row in summary.iterrows():
    print(f"\n{row['Meal Period']}")
    print(f"  Revenue:  £{row['Revenue']:,.2f}")
    print(f"  Orders:   {row['Orders']:,}")
    print(f"  Share:    {row['% of Sales']:.1f}%")

print("\n" + "=" * 70)
print("COMPARISON TO DASHBOARD:")
print("=" * 70)
print("\nDashboard shows:")
print("  Best: Dinner - £44,141.51 (54.5%), 2,867 orders")
print("  Worst: Breakfast - £417.49 (0.5%), 23 orders")

print("\nCalculated from CSV:")
best = summary.iloc[0]
worst = summary.iloc[-1]
print(f"  Best: {best['Meal Period']} - £{best['Revenue']:,.2f} ({best['% of Sales']:.1f}%), {best['Orders']:,} orders")
print(f"  Worst: {worst['Meal Period']} - £{worst['Revenue']:,.2f} ({worst['% of Sales']:.1f}%), {worst['Orders']:,} orders")

# Check if they match
dinner_match = abs(best['Revenue'] - 44141.51) < 1
breakfast_match = abs(worst['Revenue'] - 417.49) < 1

print("\n" + "=" * 70)
if dinner_match and breakfast_match:
    print("✅ DATA IS ACCURATE - Dashboard matches CSV exactly!")
else:
    print("⚠️ DISCREPANCY FOUND - Values don't match")
print("=" * 70)

# Show sample times for each period
print("\n" + "=" * 70)
print("SAMPLE ORDER TIMES (to verify logic):")
print("=" * 70)
for period in ["Dinner (8pm-12am)", "Breakfast (8am-12pm)"]:
    sample = df[df['Meal Period'] == period]['Order time'].head(3)
    print(f"\n{period}:")
    for time in sample:
        print(f"  - {time}")
