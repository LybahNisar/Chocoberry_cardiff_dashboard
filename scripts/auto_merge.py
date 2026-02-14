import pandas as pd
import glob
from pathlib import Path
import shutil
from datetime import datetime

def merge_sales_data():
    print("🔄 STARTING AUTO-MERGE PROCESS...")
    data_dir = Path('data/raw/chocoberry_cardiff')
    all_files = list(data_dir.glob('*.csv'))
    
    sales_dfs = []
    print(f"📂 Scanning {len(all_files)} files in {data_dir}...")
    
    count = 0
    for f in all_files:
        try:
            # Heuristic: Check if file looks like a sales export
            # Flipdish exports usually have 'Order ID', 'Order time', 'Revenue'
            df = pd.read_csv(f)
            required_cols = ['Order ID', 'Order time', 'Revenue']
            
            if all(col in df.columns for col in required_cols):
                print(f"   ✅ Found Sales File: {f.name} ({len(df)} rows)")
                sales_dfs.append(df)
                count += 1
            else:
                pass # Not a sales file (e.g. items csv)
        except Exception as e:
            print(f"   ⚠️ Error reading {f.name}: {e}")
            
    if not sales_dfs:
        print("❌ No matching sales data files found! Please ensure your new CSV has 'Order ID' and 'Revenue' columns.")
        return

    print(f"\n🔗 Merging {count} files...")
    merged = pd.concat(sales_dfs)
    
    # Standardize Date
    # Try dayfirst=True (British format)
    merged['Order time'] = pd.to_datetime(merged['Order time'], dayfirst=True, errors='coerce')
    
    # Deduplicate based on Order ID
    initial_rows = len(merged)
    merged = merged.drop_duplicates(subset=['Order ID'])
    final_rows = len(merged)
    
    duplicates_removed = initial_rows - final_rows
    print(f"   🧹 Removed {duplicates_removed} duplicate 'Order ID' rows.")
    
    # Sort by date
    merged = merged.sort_values('Order time')
    
    # Verify Date Range
    start_date = merged['Order time'].min()
    end_date = merged['Order time'].max()
    print(f"   📅 New Data Range: {start_date} to {end_date}")
    
    # Safety Backup
    backup_path = data_dir / f"sales_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    if (data_dir / 'sales_data.csv').exists():
        shutil.copy(data_dir / 'sales_data.csv', backup_path)
        print(f"   🛡️ Backup created: {backup_path.name}")
    
    # Save Combined File
    output_path = data_dir / 'sales_data.csv'
    merged.to_csv(output_path, index=False)
    
    print(f"\n✨ MERGE COMPLETE!")
    print(f"   Total Orders: {final_rows}")
    print(f"   File saved to: {output_path}")
    print("   👉 Please reload your dashboard to see the updated data!")

if __name__ == "__main__":
    merge_sales_data()
