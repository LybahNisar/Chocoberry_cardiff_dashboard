import pandas as pd

df = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
df['Date'] = df['Order time'].dt.date

# Feb 5-6 orders
feb5 = len(df[df['Date'] == pd.to_datetime('2026-02-05').date()])
feb6 = len(df[df['Date'] == pd.to_datetime('2026-02-06').date()])

print(f"Feb 5: {feb5} orders")
print(f"Feb 6: {feb6} orders")
print(f"Feb 5-6 total: {feb5 + feb6} orders")

# Show last 5 days
daily = df.groupby('Date').size().reset_index(name='Orders')
daily = daily.sort_values('Date')
print("\nLast 5 days:")
for _, row in daily.tail(5).iterrows():
    print(f"  {row['Date']}: {row['Orders']} orders")
