import pandas as pd
from pathlib import Path

print("🔧 DATE-BASED MERGE STRATEGY\n")

data_dir = Path('data/raw/chocoberry_cardiff')

# Load files
old = pd.read_csv(data_dir / 'sales_data_BACKUP_before_13feb.csv')
new = pd.read_csv(data_dir / 'sales_data_13feb.csv')

# Parse dates
old['Order time'] = pd.to_datetime(old['Order time'])
new['Order time'] = pd.to_datetime(new['Order time'])

print(f"OLD: {len(old)} orders ({old['Order time'].min().date()} to {old['Order time'].max().date()})")
print(f"NEW: {len(new)} orders ({new['Order time'].min().date()} to {new['Order time'].max().date()})")

# Strategy: Keep old file up to Feb 6, add new file from Feb 7 onwards
cutoff_date = pd.to_datetime('2026-02-07')

old_data = old[old['Order time'] < cutoff_date]
new_data = new[new['Order time'] >= cutoff_date]

print(f"\nKeeping from OLD file (before Feb 7): {len(old_data)} orders")
print(f"Adding from NEW file (Feb 7+): {len(new_data)} orders")

# Combine
combined = pd.concat([old_data, new_data], ignore_index=True)

# Deduplicate just in case
combined = combined.drop_duplicates(subset=['Order ID'])

# Sort
combined = combined.sort_values('Order time')

print(f"\n✅ FINAL: {len(combined)} total orders")
print(f"✅ DATE RANGE: {combined['Order time'].min().date()} to {combined['Order time'].max().date()}")

# Save
combined.to_csv(data_dir / 'sales_data.csv', index=False)
print(f"\n🎉 SUCCESS! sales_data.csv now extends to Feb 13!")
