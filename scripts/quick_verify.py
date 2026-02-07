import pandas as pd

# Load sales data
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'], errors='coerce')
df = df[df['Order time'].notna()]

# Convert numeric columns
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)
df['Tax on gross sales'] = pd.to_numeric(df['Tax on gross sales'], errors='coerce').fillna(0)
df['Delivery charges'] = pd.to_numeric(df['Delivery charges'], errors='coerce').fillna(0)

print("="*60)
print("CALCULATED FROM sales_data.csv:")
print("="*60)
print(f"Total Revenue:      {df['Revenue'].sum()/1000:.1f}K")
print(f"Average Order:      {df['Gross sales'].mean():.2f}")
print(f"Total Orders:       {len(df):,}")
print(f"Total Tax:          {df['Tax on gross sales'].sum()/1000:.1f}K")
print(f"Delivery Charges:   {df['Delivery charges'].sum():.2f}")

# Peak hours
hourly = df.groupby(df['Order time'].dt.hour)['Gross sales'].sum().sort_values(ascending=False)
print(f"\nPeak #1:            {hourly.index[0]:02d}:00 - £{hourly.iloc[0]:,.2f}")
print(f"Peak #2:            {hourly.index[1]:02d}:00 - £{hourly.iloc[1]:,.2f}")
print(f"Peak #3:            {hourly.index[2]:02d}:00 - £{hourly.iloc[2]:,.2f}")
print("="*60)
