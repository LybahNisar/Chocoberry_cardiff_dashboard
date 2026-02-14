import pandas as pd
from pathlib import Path

print("🎯 FINAL COMPREHENSIVE MERGE\n")

data_dir = Path('data/raw/chocoberry_cardiff')

# The 13feb file DOES have Feb 7-13 data!
# Strategy: Use sales_data_13feb.csv as the PRIMARY source since it's the most recent
# and supplement with older data if needed

feb13_file = pd.read_csv(data_dir / 'sales_data_13feb.csv')
feb13_file['Order time'] = pd.to_datetime(feb13_file['Order time'], errors='coerce')

print(f"sales_data_13feb.csv:")
print(f"  Rows: {len(feb13_file)}")
print(f"  Date Range: {feb13_file['Order time'].min().date()} to {feb13_file['Order time'].max().date()}")

# This file goes from Jan 31 - Feb 13
# We need Jan 4 - Jan 30 from the old files

old_file = pd.read_csv(data_dir / 'sales_data_old.csv')
old_file['Order time'] = pd.to_datetime(old_file['Order time'], errors='coerce')

print(f"\nsales_data_old.csv:")
print(f"  Rows: {len(old_file)}")
print(f"  Date Range: {old_file['Order time'].min().date()} to {old_file['Order time'].max().date()}")

# Get Jan 4-30 from old file
jan_cutoff = pd.to_datetime('2026-01-31')
old_jan = old_file[old_file['Order time'] < jan_cutoff]

print(f"\nUsing from old file (before Jan 31): {len(old_jan)} orders")
print(f"Using from 13feb file (Jan 31+): {len(feb13_file)} orders")

# Combine
final = pd.concat([old_jan, feb13_file], ignore_index=True)

# Deduplicate
final = final.drop_duplicates(subset=['Order ID'])
final = final.sort_values('Order time')

# Clean revenue
if final['Revenue'].dtype == 'object':
    final['Revenue'] = pd.to_numeric(final['Revenue'].str.replace(',', ''), errors='coerce')

print(f"\n✅ FINAL MERGED DATA:")
print(f"   Total Orders: {len(final)}")
print(f"   Unique Order IDs: {final['Order ID'].nunique()}")
print(f"   Date Range: {final['Order time'].min().date()} to {final['Order time'].max().date()}")
print(f"   Total Revenue: £{final['Revenue'].sum():,.2f}")

# Save
final.to_csv(data_dir / 'sales_data.csv', index=False)
print(f"\n🎉 SUCCESS! Saved to sales_data.csv")
