import pandas as pd

# Load and filter data
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)

# Filter: Jan 4 - Feb 4, 2026
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-04')]

# Calculate metrics
total_orders = len(df)
avg_order = df['Gross sales'].sum() / total_orders

# Peak hours
hourly = df.groupby(df['Order time'].dt.hour)['Gross sales'].sum().sort_values(ascending=False)

print("SIMPLE VERIFICATION")
print("="*50)
print(f"Total Orders: {total_orders}")
print(f"Average Order: £{avg_order:.2f}")
print(f"Peak #1: Hour {hourly.index[0]:02d}:00 = £{hourly.iloc[0]:,.2f}")
print(f"Peak #2: Hour {hourly.index[1]:02d}:00 = £{hourly.iloc[1]:,.2f}")
print(f"Peak #3: Hour {hourly.index[2]:02d}:00 = £{hourly.iloc[2]:,.2f}")
print("="*50)

# Compare to screenshot
print("\nYour Dashboard Shows:")
print("  Total Orders: 5,000")
print("  Average Order: £14.77")
print("  Peak #1 (21:00): £11,214")
print("  Peak #2 (20:00): £10,904")
print("  Peak #3 (22:00): £10,319")

print("\nMATCH CHECK:")
print(f"  Orders: {total_orders} == 5000? {total_orders == 5000}")
print(f"  Avg Order: £{avg_order:.2f} == £14.77? {abs(avg_order - 14.77) < 0.01}")
print(f"  Peak #1: £{hourly.iloc[0]:,.2f} (rounded £{round(hourly.iloc[0])}) == £11,214? {abs(hourly.iloc[0] - 11214) < 1}")
print(f"  Peak #2: £{hourly.iloc[1]:,.2f} (rounded £{round(hourly.iloc[1])}) == £10,904? {abs(hourly.iloc[1] - 10904) < 1}")
print(f"  Peak #3: £{hourly.iloc[2]:,.2f} (rounded £{round(hourly.iloc[2])}) == £10,319? {abs(hourly.iloc[2] - 10319) < 1}")

if (total_orders == 5000 and 
    abs(avg_order - 14.77) < 0.01 and 
    abs(hourly.iloc[0] - 11214) < 1 and
    abs(hourly.iloc[1] - 10904) < 1 and
    abs(hourly.iloc[2] - 10319) < 1):
    print("\n✅ VERDICT: ALL VALUES MATCH PERFECTLY")
else:
    print("\n❌ VERDICT: VALUES DO NOT MATCH")
