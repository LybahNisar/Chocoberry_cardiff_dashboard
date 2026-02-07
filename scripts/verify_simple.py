import pandas as pd

# Load data
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Convert numeric columns
for col in ['Gross sales', 'Revenue']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Filter to Jan 4 - Feb 4, 2026
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-04')]

print("DAILY SALES - First 10 Days")
print("="*60)
daily = df.groupby(df['Order time'].dt.date).agg({'Gross sales': 'sum', 'Revenue': 'sum', 'Order ID': 'count'})
for idx, row in daily.head(10).iterrows():
    print(f"{idx}: GS=£{row['Gross sales']:,.2f} Rev=£{row['Revenue']:,.2f} Orders={int(row['Order ID'])}")

print("\nDISPATCH TYPE BREAKDOWN")
print("="*60)
dispatch = df.groupby('Dispatch type').agg({'Gross sales': 'sum', 'Order ID': 'count'})
dispatch['Avg'] = dispatch['Gross sales'] / dispatch['Order ID']
for idx, row in dispatch.iterrows():
    print(f"{idx}: £{row['Gross sales']:,.2f} | {int(row['Order ID'])} orders | Avg £{row['Avg']:.2f}")

print("\nCHANNEL PERFORMANCE")
print("="*60)
channel = df.groupby('Sales channel type').agg({'Gross sales': 'sum', 'Order ID': 'count'})
total = channel['Gross sales'].sum()
channel['Share'] = (channel['Gross sales'] / total * 100)
channel['Avg'] = channel['Gross sales'] / channel['Order ID']
for idx, row in channel.sort_values('Gross sales', ascending=False).iterrows():
    print(f"{idx}: £{row['Gross sales']:,.2f} | {int(row['Order ID'])} | {row['Share']:.2f}% | Avg £{row['Avg']:.2f}")

print("\nPEAK HOURS (Top 5)")
print("="*60)
hourly = df.groupby(df['Order time'].dt.hour).agg({'Gross sales': 'sum', 'Order ID': 'count'})
for idx, row in hourly.sort_values('Gross sales', ascending=False).head(5).iterrows():
    print(f"Hour {idx:02d}:00 - £{row['Gross sales']:,.2f} | {int(row['Order ID'])} orders")
