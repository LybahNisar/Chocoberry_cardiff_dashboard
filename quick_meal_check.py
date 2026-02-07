import pandas as pd

df = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06 23:59:59')]
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Hour'] = df['Order time'].dt.hour

def categorize_meal_period(hour):
    if 8 <= hour < 12:
        return "Breakfast"
    elif 12 <= hour < 16:
        return "Lunch"
    elif 16 <= hour < 20:
        return "Evening"
    elif 20 <= hour < 24:
        return "Dinner"
    else:
        return "Night"

df['Period'] = df['Hour'].apply(categorize_meal_period)
summary = df.groupby('Period').agg({'Revenue': 'sum', 'Hour': 'count'}).reset_index()
summary.columns = ['Period', 'Revenue', 'Orders']
summary = summary.sort_values('Revenue', ascending=False)

print("Meal Period Results:")
print(f"\nBest: {summary.iloc[0]['Period']} - £{summary.iloc[0]['Revenue']:,.2f}, {summary.iloc[0]['Orders']} orders")
print(f"Worst: {summary.iloc[-1]['Period']} - £{summary.iloc[-1]['Revenue']:,.2f}, {summary.iloc[-1]['Orders']} orders")

print("\nDashboard shows:")
print("Best: Dinner - £44,141.51, 2,867 orders")
print("Worst: Breakfast - £417.49, 23 orders")

dinner_ok = abs(summary.iloc[0]['Revenue'] - 44141.51) < 1
breakfast_ok = abs(summary.iloc[-1]['Revenue'] - 417.49) < 1

if dinner_ok and breakfast_ok:
    print("\n✅ ACCURATE - Numbers match exactly!")
else:
    print("\n⚠️ Mismatch found")
