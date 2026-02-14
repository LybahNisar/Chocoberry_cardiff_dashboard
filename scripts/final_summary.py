import pandas as pd
from pathlib import Path

# Load and verify
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
df['Revenue'] = pd.to_numeric(df['Revenue'].astype(str).str.replace(',', ''), errors='coerce')

# Complete data (Jan 4 - Feb 12)
complete = df[df['Order time'].dt.date <= pd.to_datetime('2026-02-12').date()]

# Key metrics
print("FINAL AUDIT RESULTS:")
print(f"Total rows: {len(df)}")
print(f"Date range: {df['Order time'].min().date()} to {df['Order time'].max().date()}")
print(f"Duplicates: {df['Order ID'].duplicated().sum()}")
print(f"Complete data (Jan 4-Feb 12): {len(complete)} orders")
print(f"Revenue (Jan 4-Feb 12): £{complete['Revenue'].sum():,.2f}")
print(f"Avg order value: £{complete['Revenue'].mean():.2f}")
print(f"Days: {(complete['Order time'].max() - complete['Order time'].min()).days + 1}")
