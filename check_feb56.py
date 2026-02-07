import pandas as pd

# Load the merged sales_data.csv
df = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Convert to just date for easier grouping
df['Date'] = df['Order time'].dt.date

# Get orders for Feb 5-6
feb5 = df[df['Date'] == pd.to_datetime('2026-02-05').date()]
feb6 = df[df['Date'] == pd.to_datetime('2026-02-06').date()]

print("=" * 60)
print("ORDERS FOR FEB 5-6, 2026")
print("=" * 60)
print(f"\nFeb 5, 2026: {len(feb5):,} orders")
print(f"Feb 6, 2026: {len(feb6):,} orders")
print(f"Total (Feb 5-6): {len(feb5) + len(feb6):,} orders")

# Get daily breakdown for entire range
print("\n" + "=" * 60)
print("DAILY ORDER BREAKDOWN: JAN 4 - FEB 6")
print("=" * 60)

daily = df.groupby('Date').size().reset_index(name='Orders')
daily = daily[(daily['Date'] >= pd.to_datetime('2026-01-04').date()) & 
              (daily['Date'] <= pd.to_datetime('2026-02-06').date())]

print(f"\nShowing last 10 days of data:\n")
for _, row in daily.tail(10).iterrows():
    date_str = row['Date'].strftime('%b %d, %Y')
    print(f"{date_str}: {row['Orders']:,} orders")

# Totals
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
total_orders = daily['Orders'].sum()
print(f"\nTotal orders (Jan 4 - Feb 6): {total_orders:,}")
print(f"Date range: {daily['Date'].min()} to {daily['Date'].max()}")
print(f"Days with data: {len(daily)}")

# Check if we have Feb 5 and Feb 6
has_feb5 = len(feb5) > 0
has_feb6 = len(feb6) > 0

print(f"\nData completeness:")
print(f"  Feb 5 data: {'✅ YES' if has_feb5 else '❌ MISSING'}")
print(f"  Feb 6 data: {'✅ YES' if has_feb6 else '❌ MISSING'}")

if has_feb5 and has_feb6:
    print("\n✅ ACCURATE: Data includes Feb 5-6 from the NEW file")
else:
    print("\n⚠️  WARNING: Missing Feb 5-6 data")

print("=" * 60)
