"""
Inspector: Understand ALL CSV files before merging.
Identifies: date coverage, row count, columns, duplicates across files.
"""
import pandas as pd
import glob
from pathlib import Path

RAW = Path("data/raw/chocoberry_cardiff")

# Only look at the actual sales_data CSVs (not summary reports)
candidates = [
    "sales_data.csv",
    "sales_data_13feb.csv",
    "sales_data_21feb.csv",
    "sales_data_BACKUP_FINAL.csv",
    "sales_data_BACKUP_before_13feb.csv",
]

dfs = {}
for name in candidates:
    path = RAW / name
    if not path.exists():
        print(f"[MISSING] {name}")
        continue
    try:
        df = pd.read_csv(path)
        # Find the date/time column
        time_col = None
        for c in df.columns:
            if "order" in c.lower() and "time" in c.lower():
                time_col = c
                break
        
        if time_col:
            df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
            start = df[time_col].min()
            end   = df[time_col].max()
        else:
            start = end = "N/A"
        
        id_col = None
        for c in df.columns:
            if "order" in c.lower() and "id" in c.lower():
                id_col = c
                break
        
        uniq_ids = df[id_col].nunique() if id_col else "N/A"
        nan_ids  = df[id_col].isna().sum() if id_col else "N/A"
        
        print(f"\n{'='*55}")
        print(f"FILE : {name}")
        print(f"Rows : {len(df):,}")
        print(f"Cols : {len(df.columns)}")
        print(f"ID col: {id_col}  |  Unique IDs: {uniq_ids}  |  NaN IDs: {nan_ids}")
        print(f"Start: {start}")
        print(f"End  : {end}")
        print(f"Cols : {list(df.columns[:6])} ...")
        
        dfs[name] = df
    except Exception as e:
        print(f"[ERROR] {name}: {e}")

print(f"\n\n{'='*55}")
print("CROSS-FILE DUPLICATE ANALYSIS")
print(f"{'='*55}")
if len(dfs) > 1:
    all_ids = {}
    for name, df in dfs.items():
        id_col = None
        for c in df.columns:
            if "order" in c.lower() and "id" in c.lower():
                id_col = c
                break
        if id_col:
            ids = set(df[id_col].dropna().astype(str))
            all_ids[name] = ids
    
    names = list(all_ids.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            overlap = len(all_ids[names[i]] & all_ids[names[j]])
            print(f"  Overlap ({names[i]} <-> {names[j]}): {overlap} duplicate order IDs")
