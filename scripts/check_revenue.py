import pandas as pd

df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Clean revenue
if df['Revenue'].dtype == 'object':
    df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')

print(f'CSV File Stats:')
print(f'  Total Orders: {len(df)}')
print(f'  Total Revenue: £{df["Revenue"].sum():,.2f}')
print(f'  Date Range: {df["Order time"].min().date()} to {df["Order time"].max().date()}')

# Check if dashboard might be using "Gross sales" instead
if 'Gross sales' in df.columns:
    if df['Gross sales'].dtype == 'object':
        df['Gross sales'] = pd.to_numeric(df['Gross sales'].str.replace(',', ''), errors='coerce')
    print(f'\nGross Sales Total: £{df["Gross sales"].sum():,.2f}')
