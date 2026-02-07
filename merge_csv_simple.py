import pandas as pd
from pathlib import Path

# Simple CSV Merge - Debug Version
print("=" * 60)
print("CSV MERGE - Debug Mode")
print("=" * 60)

# Paths
data_path = Path("C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff")
old_file = data_path / "sales_data_old.csv"
new_file = data_path / "sales_data_new.csv"
output_file = data_path / "sales_data.csv"

try:
    # Step 1: Load old data
    print(f"\n1. Loading: {old_file.name}")
    old_df = pd.read_csv(old_file)
    print(f"   ✅ {len(old_df)} rows loaded")
    
    # Step 2: Load new data
    print(f"\n2. Loading: {new_file.name}")
    new_df = pd.read_csv(new_file)
    print(f"   ✅ {len(new_df)} rows loaded")
    
    # Step 3: Combine
    print(f"\n3. Combining data...")
    combined = pd.concat([old_df, new_df], ignore_index=True)
    print(f"   Total: {len(combined)} rows")
    
    # Step 4: Remove duplicates
    print(f"\n4. Removing duplicates by Order ID...")
    before = len(combined)
    combined = combined.drop_duplicates(subset=['Order ID'], keep='first')
    removed = before - len(combined)
    print(f"   Removed: {removed} duplicates")
    print(f"   Final: {len(combined)} unique rows")
    
    # Step 5: Sort by Order time
    print(f"\n5. Sorting by Order time...")
    combined['Order time'] = pd.to_datetime(combined['Order time'], errors='coerce')
    combined = combined.sort_values('Order time')
    
    # Step 6: Save
    print(f"\n6. Saving to: {output_file.name}")
    combined.to_csv(output_file, index=False)
    print(f"   ✅ SAVED!")
    
    # Step 7: Summary
    print("\n" + "=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print(f"Final file: {output_file}")
    print(f"Total rows: {len(combined):,}")
    
    # Show date range
    min_date = combined['Order time'].min()
    max_date = combined['Order time'].max()
    print(f"Date range: {min_date.date()} to {max_date.date()}")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
