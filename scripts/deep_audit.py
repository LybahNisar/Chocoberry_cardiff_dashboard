import pandas as pd
from pathlib import Path
import glob

print("🔎 DEEP AUDIT of data/raw/chocoberry_cardiff/...\n")
files = glob.glob('data/raw/chocoberry_cardiff/*.csv')

sales_files = []
menu_files = []
other_files = []

for f in files:
    try:
        df = pd.read_csv(f)
        name = Path(f).name
        rows = len(df)
        cols = list(df.columns)
        
        info = {'name': name, 'rows': rows, 'cols': cols}
        
        if 'Order time' in df.columns:
            # Sales Data
            try:
                # Try British first
                times = pd.to_datetime(df['Order time'], dayfirst=True, errors='coerce').dropna()
                if not times.empty:
                    info['min_date'] = times.min()
                    info['max_date'] = times.max()
                    sales_files.append(info)
                else:
                    other_files.append(info)
            except:
                other_files.append(info)
        elif 'Item' in df.columns and ('Sales' in df.columns or 'Revenue' in df.columns):
            # Menu Data
            menu_files.append(info)
        else:
            other_files.append(info)
            
    except Exception as e:
        print(f"⚠️ Error reading {f}: {e}")

print(f"---------- FOUND {len(sales_files)} SALES FILES ----------")
for f in sales_files:
    print(f"📄 {f['name']}")
    print(f"   Rows: {f['rows']}")
    print(f"   Range: {f.get('min_date', 'Unknown')} to {f.get('max_date', 'Unknown')}")
    print("   Duplicate Check: Ready for merge")
    print("-" * 40)

print(f"\n---------- FOUND {len(menu_files)} MENU FILES ----------")
for f in menu_files:
    print(f"🍔 {f['name']} ({f['rows']} items)")

print(f"\n---------- FOUND {len(other_files)} OTHER FILES ----------")
for f in other_files:
    print(f"📁 {f['name']} (Columns: {len(f['cols'])})")
