import pandas as pd

print("🔍 Checking sales_data_new.csv for Feb 7-13 data:\n")

new = pd.read_csv('data/raw/chocoberry_cardiff/sales_data_new.csv')
new['Order time'] = pd.to_datetime(new['Order time'])

print(f"Total rows: {len(new)}")
print(f"Date range: {new['Order time'].min().date()} to {new['Order time'].max().date()}")

feb7_plus = new[new['Order time'] >= '2026-02-07']
print(f"\nOrders from Feb 7-13: {len(feb7_plus)}")

if len(feb7_plus) > 0:
    print(f"Sample Order IDs from Feb 7+: {feb7_plus['Order ID'].head(5).tolist()}")
