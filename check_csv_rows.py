import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

print(f"Total rows in sales_data.csv: {len(df)}")

filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]
print(f"Rows for Jan 4 - Feb 6: {len(filtered)}")
print(f"First date in file: {df['Order time'].min()}")
print(f"Last date in file: {df['Order time'].max()}")
