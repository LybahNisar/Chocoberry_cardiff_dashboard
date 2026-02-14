import pandas as pd
from pathlib import Path

print("🔧 CORRECT MERGE STRATEGY\n")

data_dir = Path('data/raw/chocoberry_cardiff')

# The key insight: sales_data_13feb.csv is Jan 31 - Feb 13
# The old file is Jan 4 - Feb 6
# We need: Jan 4 - Jan 30 from OLD + Jan 31 - Feb 13 from NEW

old = pd.read_csv(data_dir / 'sales_data_BACKUP_before_13feb.csv')
new = pd.read_csv(data_dir / 'sales_data_13feb.csv')

old['Order time'] = pd.to_datetime(old['Order time'])
new['Order time'] = pd.to_datetime(new['Order time'])

print(f"OLD file: {len(old)} orders ({old['Order time'].min().date()} to {old['Order time'].max().date()})")
print(f"NEW file: {len(new)} orders ({new['Order time'].min().date()} to {new['Order time'].max().date()})")

# Strategy: Keep Jan 4-30 from old, use Jan 31+ from new
cutoff = pd.to_datetime('2026-01-31')

old_early = old[old['Order time'] < cutoff]
new_late = new[new['Order time'] >= cutoff]

print(f"\nKeeping from OLD (Jan 4-30): {len(old_early)} orders")
print(f"Adding from NEW (Jan 31-Feb 13): {len(new_late)} orders")

combined = pd.concat([old_early, new_late], ignore_index=True)
combined = combined.drop_duplicates(subset=['Order ID'])
combined = combined.sort_values('Order time')

# Clean revenue
if combined['Revenue'].dtype == 'object':
    combined['Revenue'] = pd.to_numeric(combined['Revenue'].str.replace(',', ''), errors='coerce')

print(f"\n✅ FINAL: {len(combined)} orders")
print(f"✅ DATE RANGE: {combined['Order time'].min().date()} to {combined['Order time'].max().date()}")
print(f"✅ REVENUE: £{combined['Revenue'].sum():,.2f}")

combined.to_csv(data_dir / 'sales_data.csv', index=False)
print("\n🎉 Merge complete!")
