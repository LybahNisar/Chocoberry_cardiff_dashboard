import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

print('✅ FINAL VERIFICATION:')
print(f'   Orders: {len(df)}')
print(f'   Date Range: {df["Order time"].min().date()} to {df["Order time"].max().date()}')
print(f'   Unique IDs: {df["Order ID"].nunique()}')

if df['Revenue'].dtype == 'object':
    df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')
    
print(f'   Total Revenue: £{df["Revenue"].sum():,.2f}')
