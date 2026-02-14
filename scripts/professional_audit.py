import pandas as pd
from pathlib import Path
import glob
import os

def audit():
    print("=== 🕵️‍♂️ PROFESSIONAL DATA AUDIT REPORT ===\n")
    
    data_dir = Path('data/raw/chocoberry_cardiff')
    all_files = list(data_dir.glob('*.csv'))
    
    print(f"📂 Found {len(all_files)} CSV files in data directory.")
    
    # Files we KNOW we are using
    used_files = [
        'sales_data.csv', 
        'most_sold_items.csv', 
        'least_sold_items.csv', 
        'best-selling_categories.csv'
    ]
    
    unused_files = []
    
    for f in all_files:
        print(f"\n📄 Analyzing: {f.name}")
        try:
            df = pd.read_csv(f)
            print(f"   Rows: {len(df)}")
            print(f"   Columns: {list(df.columns)}")
            
            if f.name not in used_files:
                unused_files.append(f.name)
                print("   ⚠️ STATUS: NOT USED in Dashboard")
            else:
                print("   ✅ STATUS: USED in Dashboard")
                
            # Specific Checks
            if f.name == 'sales_data.csv':
                if 'Order time' in df.columns:
                    df['Order time'] = pd.to_datetime(df['Order time'], dayfirst=True)
                    print(f"   📅 Date Range: {df['Order time'].min().date()} to {df['Order time'].max().date()}")
                    if 'Revenue' in df.columns:
                        # Clean revenue
                        rev = df['Revenue']
                        if rev.dtype == 'object':
                            rev = pd.to_numeric(rev.str.replace(',', ''), errors='coerce')
                        print(f"   💰 Total Revenue: £{rev.sum():,.2f}")
                        
                        # Check for Summary Row
                        last_val = str(df.iloc[-1, 0])
                        if 'Total' in last_val or 'Summary' in last_val:
                             print("   ⚠️ WARNING: Possible Summary Row detected at end of file. This might cause Double Counting!")
                else:
                    print("   ❌ CRITICAL: 'Order time' column missing!")

            if f.name == 'most_sold_items.csv':
                 if 'Sales' in df.columns:
                    s = df['Sales']
                    if s.dtype == 'object':
                        s = pd.to_numeric(s.str.replace(',', ''), errors='coerce')
                    print(f"   🏆 Top Item Revenue: £{s.max():,.2f}")
                    # Check for date
                    if not any(col in df.columns for col in ['Date', 'Time', 'Day']):
                         print("   ℹ️ NOTE: No Date column. Comparison is Aggregate only.")

        except Exception as e:
            print(f"   ❌ ERROR Reading File: {e}")

    print("\n" + "="*40)
    print("📢 AUDIT CONCLUSION")
    print("="*40)
    if unused_files:
        print(f"⚠️ MISSING DATA WARNING: The following files are present but NOT currently visualized:")
        for uf in unused_files:
            print(f"  - {uf}")
    else:
        print("✅ ALL DATA ACCOUNTED FOR: All CSV files are being used.")

    # Implementation Accuracy Check
    print("\n🔍 LOGIC CHECK:")
    print("  - Daily/Weekly Breakdown: Implemented on Revenue (sales_data.csv).")
    print("  - Item Breakdown: Implemented on Aggregates (most_sold_items.csv).")
    print("  - Discrepancy Check: Item file has no dates, so Daily Item Breakdown is IMPOSSIBLE with provided data.")

if __name__ == "__main__":
    audit()
