import pandas as pd
from pathlib import Path

print("🔧 FORCED MERGE: Including sales_data_13feb.csv\n")

data_dir = Path('data/raw/chocoberry_cardiff')

# Load the three key files
old = pd.read_csv(data_dir / 'sales_data.csv')
new = pd.read_csv(data_dir / 'sales_data_13feb.csv')

print(f"OLD file: {len(old)} rows")
print(f"NEW file: {len(new)} rows")

# Combine
combined = pd.concat([old, new], ignore_index=True)
print(f"Combined (before dedup): {len(combined)} rows")

# Deduplicate
combined = combined.drop_duplicates(subset=['Order ID'])
print(f"After deduplication: {len(combined)} rows")

# Parse dates
combined['Order time'] = pd.to_datetime(combined['Order time'], errors='coerce')

# Sort
combined = combined.sort_values('Order time')

# Verify range
print(f"\n✅ NEW DATE RANGE: {combined['Order time'].min()} to {combined['Order time'].max()}")

# Backup old file
import shutil
backup_path = data_dir / 'sales_data_BACKUP_before_13feb.csv'
shutil.copy(data_dir / 'sales_data.csv', backup_path)
print(f"📦 Backup saved: {backup_path.name}")

# Save
combined.to_csv(data_dir / 'sales_data.csv', index=False)
print(f"\n🎉 SUCCESS! Updated sales_data.csv with {len(combined)} total orders")
