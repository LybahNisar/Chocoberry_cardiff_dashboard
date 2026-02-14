import pandas as pd
from pathlib import Path

print("🔧 MERGING ALL 4 SALES FILES\n")

data_dir = Path('data/raw/chocoberry_cardiff')

# Load all files
files = {
    'old': 'sales_data_old.csv',
    'current': 'sales_data.csv',
    'feb13': 'sales_data_13feb.csv',
    'new': 'sales_data_new.csv'
}

dfs = []
for name, filename in files.items():
    filepath = data_dir / filename
    if filepath.exists():
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {filename}: {len(df)} rows")
        dfs.append(df)
    else:
        print(f"❌ {filename} not found")

if not dfs:
    print("ERROR: No files found!")
    exit(1)

# Combine all
print(f"\n🔗 Combining {len(dfs)} files...")
combined = pd.concat(dfs, ignore_index=True)
print(f"   Before dedup: {len(combined)} rows")

# Deduplicate by Order ID
combined = combined.drop_duplicates(subset=['Order ID'], keep='last')
print(f"   After dedup: {len(combined)} rows")

# Parse and sort by date
combined['Order time'] = pd.to_datetime(combined['Order time'], errors='coerce')
combined = combined.sort_values('Order time')

# Clean revenue
if combined['Revenue'].dtype == 'object':
    combined['Revenue'] = pd.to_numeric(combined['Revenue'].str.replace(',', ''), errors='coerce')

print(f"\n✅ FINAL MERGED DATA:")
print(f"   Total Orders: {len(combined)}")
print(f"   Date Range: {combined['Order time'].min().date()} to {combined['Order time'].max().date()}")
print(f"   Total Revenue: £{combined['Revenue'].sum():,.2f}")
print(f"   Unique Order IDs: {combined['Order ID'].nunique()}")

# Backup current file
import shutil
backup_path = data_dir / 'sales_data_BACKUP_FINAL.csv'
if (data_dir / 'sales_data.csv').exists():
    shutil.copy(data_dir / 'sales_data.csv', backup_path)
    print(f"\n📦 Backup saved: {backup_path.name}")

# Save
output_path = data_dir / 'sales_data.csv'
combined.to_csv(output_path, index=False)
print(f"\n🎉 SUCCESS! Saved to {output_path.name}")
