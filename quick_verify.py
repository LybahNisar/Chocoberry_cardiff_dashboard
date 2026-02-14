import pandas as pd
from pathlib import Path

# Load data
data_path = Path('data/raw/chocoberry_cardiff')
df = pd.read_csv(data_path / 'sales_data.csv')

# Convert to numeric
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)
df['Revenue after refunds'] = pd.to_numeric(df['Revenue after refunds'], errors='coerce').fillna(0)
df['Refunds'] = pd.to_numeric(df['Refunds'], errors='coerce').fillna(0)
df['Order time'] = pd.to_datetime(df['Order time'])

# Filter date range
filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]

print("=" * 60)
print("QUICK CSV VERIFICATION")
print("=" * 60)
print(f"\nTotal Orders: {len(filtered):,}")
print(f"Total Gross Sales: £{filtered['Gross sales'].sum():,.2f}")
print(f"Total Revenue (after refunds): £{filtered['Revenue after refunds'].sum():,.2f}")
print(f"Total Refunds: £{filtered['Refunds'].sum():,.2f}")
print(f"Average Order Value: £{(filtered['Gross sales'].sum() / len(filtered)):.2f}")
print(f"Refund Rate: {(filtered['Refunds'].sum() / filtered['Gross sales'].sum() * 100):.2f}%")
print()

# Check dispatch types
print("Dispatch Type Breakdown:")
dispatch = filtered.groupby('Dispatch type').agg({
    'Revenue after refunds': 'sum',
    'Order time': 'count'
})
dispatch.columns = ['Revenue', 'Orders']
print(dispatch)
print()

# Check meal periods
df_filtered = filtered.copy()
df_filtered['hour'] = df_filtered['Order time'].dt.hour

def get_meal_period(hour):
    if 8 <= hour < 12:
        return "Breakfast"
    elif 12 <= hour < 16:
        return "Lunch"
    elif 16 <= hour < 20:
        return "Evening"
    elif 20 <= hour < 24:
        return "Dinner"
    else:
        return "Night Shift"

df_filtered['meal_period'] = df_filtered['hour'].apply(get_meal_period)
meal = df_filtered.groupby('meal_period')['Revenue after refunds'].sum().sort_values(ascending=False)

print("Meal Period Revenue:")
for period, rev in meal.items():
    print(f"  {period}: £{rev:,.2f}")
