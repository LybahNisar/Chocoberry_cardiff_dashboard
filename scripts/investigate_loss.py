import pandas as pd

print("🔍 INVESTIGATING DATA LOSS\n")

# Check backup (original file)
backup = pd.read_csv('data/raw/chocoberry_cardiff/sales_data_BACKUP_before_13feb.csv')
backup['Order time'] = pd.to_datetime(backup['Order time'])

# Clean revenue column
if backup['Revenue'].dtype == 'object':
    backup['Revenue'] = pd.to_numeric(backup['Revenue'].str.replace(',', ''), errors='coerce')

print("ORIGINAL FILE (Before merge):")
print(f"  Rows: {len(backup)}")
print(f"  Date range: {backup['Order time'].min().date()} to {backup['Order time'].max().date()}")
print(f"  Revenue: £{backup['Revenue'].sum():,.2f}")

# Check current file
current = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
current['Order time'] = pd.to_datetime(current['Order time'])

if current['Revenue'].dtype == 'object':
    current['Revenue'] = pd.to_numeric(current['Revenue'].str.replace(',', ''), errors='coerce')

print("\nCURRENT FILE (After merge):")
print(f"  Rows: {len(current)}")
print(f"  Date range: {current['Order time'].min().date()} to {current['Order time'].max().date()}")
print(f"  Revenue: £{current['Revenue'].sum():,.2f}")

# Check what was lost
print(f"\n⚠️ DIFFERENCE:")
print(f"  Lost rows: {len(backup) - len(current)}")
print(f"  Lost revenue: £{backup['Revenue'].sum() - current['Revenue'].sum():,.2f}")
