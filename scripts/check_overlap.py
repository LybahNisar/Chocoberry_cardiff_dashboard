import pandas as pd

old = pd.read_csv('data/raw/chocoberry_cardiff/sales_data_BACKUP_before_13feb.csv')
new = pd.read_csv('data/raw/chocoberry_cardiff/sales_data_13feb.csv')

overlap = set(old['Order ID']) & set(new['Order ID'])

print(f'Old file unique Order IDs: {old["Order ID"].nunique()}')
print(f'New file unique Order IDs: {new["Order ID"].nunique()}')
print(f'Overlapping Order IDs: {len(overlap)}')
print(f'Truly NEW Order IDs in 13feb file: {new["Order ID"].nunique() - len(overlap)}')

# Check dates in new file
new['Order time'] = pd.to_datetime(new['Order time'])
print(f'\nNew file date range: {new["Order time"].min()} to {new["Order time"].max()}')

# Check if new file has Feb 7-13 data
feb_7_plus = new[new['Order time'] >= '2026-02-07']
print(f'Orders after Feb 6 in new file: {len(feb_7_plus)}')
