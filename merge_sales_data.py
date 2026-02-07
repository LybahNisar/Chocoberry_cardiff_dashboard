import pandas as pd
from pathlib import Path

"""
CSV MERGE SCRIPT - Combine Historical Sales Data
================================================
This script merges old and new CSV exports to build historical data.
Flipdish limits exports to 31 days, but this script lets you keep ALL data over time.
"""

# ============================================================================
# CONFIGURATION
# ============================================================================

# Path to your dashboard data folder
DATA_PATH = Path(__file__).parent / 'data' / 'raw' / 'chocoberry_cardiff'

# Name your CSV files
OLD_CSV = 'sales_data_old.csv'  # Rename your old CSV to this
NEW_CSV = 'sales_data_new.csv'  # Rename your new CSV to this
MERGED_CSV = 'sales_data.csv'   # This will be the combined file

# ============================================================================
# MERGE FUNCTION
# ============================================================================

def merge_sales_data():
    """Merge old and new sales CSV files, removing duplicates."""
    
    print("=" * 60)
    print("CSV MERGE SCRIPT - Starting...")
    print("=" * 60)
    
    # Load old data
    print(f"\n1. Loading old data from: {OLD_CSV}")
    old_file = DATA_PATH / OLD_CSV
    
    if not old_file.exists():
        print(f"   ❌ ERROR: {OLD_CSV} not found!")
        print(f"   Please rename your old CSV file to '{OLD_CSV}'")
        return
    
    old_data = pd.read_csv(old_file)
    print(f"   ✅ Loaded {len(old_data)} rows from old file")
    print(f"   Date range: {old_data['Order time'].min()} to {old_data['Order time'].max()}")
    
    # Load new data
    print(f"\n2. Loading new data from: {NEW_CSV}")
    new_file = DATA_PATH / NEW_CSV
    
    if not new_file.exists():
        print(f"   ❌ ERROR: {NEW_CSV} not found!")
        print(f"   Please rename your new CSV file to '{NEW_CSV}'")
        return
    
    new_data = pd.read_csv(new_file)
    print(f"   ✅ Loaded {len(new_data)} rows from new file")
    print(f"   Date range: {new_data['Order time'].min()} to {new_data['Order time'].max()}")
    
    # Combine data
    print("\n3. Merging data...")
    combined = pd.concat([old_data, new_data], ignore_index=True)
    print(f"   Combined total: {len(combined)} rows")
    
    # Remove duplicates based on Order ID
    print("\n4. Removing duplicates...")
    before_count = len(combined)
    combined = combined.drop_duplicates(subset=['Order ID'], keep='first')
    duplicates_removed = before_count - len(combined)
    print(f"   Removed {duplicates_removed} duplicate orders")
    print(f"   Final count: {len(combined)} unique orders")
    
    # Sort by date
    print("\n5. Sorting by date...")
    combined['Order time'] = pd.to_datetime(combined['Order time'], errors='coerce')
    combined = combined.sort_values('Order time')
    combined = combined.dropna(subset=['Order time'])  # Remove any rows with invalid dates
    
    # Save merged file
    print(f"\n6. Saving merged data to: {MERGED_CSV}")
    output_file = DATA_PATH / MERGED_CSV
    combined.to_csv(output_file, index=False)
    print(f"   ✅ Saved successfully!")
    
    # Show final date range
    print("\n" + "=" * 60)
    print("MERGE COMPLETE!")
    print("=" * 60)
    print(f"Total orders: {len(combined):,}")
    print(f"Date range: {combined['Order time'].min()} to {combined['Order time'].max()}")
    print(f"\nYour dashboard will now show data from {combined['Order time'].min().date()} to {combined['Order time'].max().date()}")
    print("\nNext time you export new data from Flipdish:")
    print("1. Rename current sales_data.csv to sales_data_old.csv")
    print("2. Save new export as sales_data_new.csv")
    print("3. Run this script again")
    print("=" * 60)

# ============================================================================
# RUN THE SCRIPT
# ============================================================================

if __name__ == "__main__":
    try:
        merge_sales_data()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPlease check:")
        print("1. Both CSV files are in the data/raw/chocoberry_cardiff folder")
        print("2. Files are named correctly (sales_data_old.csv and sales_data_new.csv)")
        print("3. CSV files have the same column structure")
