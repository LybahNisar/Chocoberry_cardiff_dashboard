import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

daily = df.groupby(df['Order time'].dt.date).size()

print('Orders per day (last 10 days):')
for date, count in daily.tail(10).items():
    print(f'{date}: {count} orders')

print(f'\nTotal orders Feb 7-13:')
feb_7_13 = df[(df['Order time'].dt.date >= pd.to_datetime('2026-02-07').date()) & 
              (df['Order time'].dt.date <= pd.to_datetime('2026-02-13').date())]
print(f'{len(feb_7_13)} orders')

print(f'\nBreakdown Feb 7-13:')
for date, count in feb_7_13.groupby(feb_7_13['Order time'].dt.date).size().items():
    print(f'{date}: {count} orders')
