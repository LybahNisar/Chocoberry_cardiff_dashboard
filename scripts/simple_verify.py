import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Jan 4 - Feb 12
jan4_feb12 = df[(df['Order time'].dt.date >= pd.to_datetime('2026-01-04').date()) & 
                (df['Order time'].dt.date <= pd.to_datetime('2026-02-12').date())]

print(f'Jan 4 - Feb 12 Orders: {len(jan4_feb12)}')
print(f'Date Range: {jan4_feb12["Order time"].min().date()} to {jan4_feb12["Order time"].max().date()}')
print(f'Total Days: {(jan4_feb12["Order time"].max() - jan4_feb12["Order time"].min()).days + 1}')
print(f'Average Orders/Day: {len(jan4_feb12) / ((jan4_feb12["Order time"].max() - jan4_feb12["Order time"].min()).days + 1):.0f}')
