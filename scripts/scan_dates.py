import pandas as pd
from pathlib import Path
import glob

print("Scanning for date ranges...")
files = glob.glob('data/raw/chocoberry_cardiff/*.csv')

for f in files:
    try:
        df = pd.read_csv(f)
        if 'Order time' in df.columns:
            # Try parsing with dayfirst=True for UK formats
            times = pd.to_datetime(df['Order time'], dayfirst=True, errors='coerce')
            
            # Check valid dates
            valid_times = times.dropna()
            if not valid_times.empty:
                print(f"📄 {Path(f).name}: {valid_times.min().date()} to {valid_times.max().date()} (Rows: {len(df)})")
            else:
                 print(f"📄 {Path(f).name}: Has 'Order time' but no valid dates found.")
    except Exception as e:
        pass
