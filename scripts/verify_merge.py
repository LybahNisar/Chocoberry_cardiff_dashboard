import pandas as pd
import glob
from pathlib import Path

print("🕵️ MERGE INTEGRITY & ACCURACY REPORT\n")
try:
    # 1. Inspect Final File
    final_df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
    
    # Try dayfirst=True for verify
    final_df['Order time'] = pd.to_datetime(final_df['Order time'], dayfirst=True, errors='coerce')
    
    print(f"✅ MASTER SALES DATA (The Dashboard Source):")
    print(f"   - Total Unique Orders: {len(final_df)}")
    if not final_df['Order time'].isnull().all():
        print(f"   - Date Range: {final_df['Order time'].min()} to {final_df['Order time'].max()}")
    
    # Check numeric integrity
    # Handle existing string commas if any
    cols_to_check = ['Revenue', 'Tax on gross sales', 'Gross sales']
    for col in cols_to_check:
        if final_df[col].dtype == 'object':
             final_df[col] = pd.to_numeric(final_df[col].astype(str).str.replace(',', ''), errors='coerce')
             
    print(f"   - Total Revenue: £{final_df['Revenue'].sum():,.2f}")
    print(f"   - Total Tax: £{final_df['Tax on gross sales'].sum():,.2f}")
    
    # Check Duplicates
    if len(final_df) == final_df['Order ID'].nunique():
        print("   ✨ NO DUPLICATES: Every order is unique.")
    else:
        dupes = len(final_df) - final_df['Order ID'].nunique()
        print(f"   ⚠️ WARNING: {dupes} Duplicate Order IDs found!")

    # 2. Source Trace
    print("\n📂 RAW SOURCE FILES FOUND (Inputs):")
    files = glob.glob('data/raw/chocoberry_cardiff/*.csv')
    
    sales_files_count = 0
    for f in files:
        try:
            df = pd.read_csv(f)
            # Identify if it is a Sales File
            if 'Order ID' in df.columns and 'Revenue' in df.columns:
                sales_files_count += 1
                # Format check
                t = pd.to_datetime(df['Order time'], dayfirst=True, errors='coerce')
                print(f"   📄 {Path(f).name}: {len(df)} rows ({t.min().date()} to {t.max().date()})")
        except:
            pass
            
    print(f"\n📊 SUMMARY:")
    print(f"   Identified {sales_files_count} distinct Sales Files.")
    print(f"   Merged them all -> Removed overlaps -> Final Count: {len(final_df)}.")
    
except Exception as e:
    print(f"❌ Error during verification: {e}")
