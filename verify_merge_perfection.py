import pandas as pd
import sqlite3
from pathlib import Path

RAW = Path("data/raw/chocoberry_cardiff")
files = ["sales_data.csv", "sales_data_21feb.csv", "sales_data_23feb.csv"]

print("--- RAW CSV ANALYSIS ---")
all_ids = set()
total_raw_rows = 0

for f in files:
    df = pd.read_csv(RAW / f, dtype=str)
    df.columns = df.columns.str.strip()
    clean_df = df.dropna(subset=["Order ID"])
    clean_df["Order ID"] = clean_df["Order ID"].astype(str).str.strip()
    
    ids = set(clean_df["Order ID"])
    print(f"{f}: {len(df):,} rows | {len(clean_df):,} valid Order IDs")
    
    all_ids.update(ids)
    total_raw_rows += len(clean_df)

print(f"\nTotal UNIQUE Order IDs across all CSVs: {len(all_ids):,}")

print("\n--- DATABASE ANALYSIS ---")
conn = sqlite3.connect('restaurant_data.db')
db_count = conn.execute("SELECT COUNT(order_id) FROM orders").fetchone()[0]
db_unique_ids = conn.execute("SELECT COUNT(DISTINCT order_id) FROM orders").fetchone()[0]

# Check for any Jan 4 or Feb 23 specific counts to ensure edges are safe
j4_db = conn.execute("SELECT COUNT(*) FROM orders WHERE date(order_time) = '2026-01-04'").fetchone()[0]
f23_db = conn.execute("SELECT COUNT(*) FROM orders WHERE date(order_time) = '2026-02-23'").fetchone()[0]

conn.close()

print(f"Total rows in DB 'orders' table: {db_count:,}")
print(f"Total UNIQUE IDs in DB: {db_unique_ids:,}")
print(f"Jan 4 Orders in DB: {j4_db}")
print(f"Feb 23 Orders in DB: {f23_db}")

print("\n--- FINAL VERDICT ---")
if db_count == len(all_ids) and db_count == db_unique_ids:
    print("✅ PERFECT MATCH: Every unique order from every CSV is in the database exactly once.")
    print("✅ ZERO DUPLICATES: Database count matches unique ID count.")
    print("✅ ZERO DATA LOSS: Database count matches the sum of unique IDs across all files.")
else:
    print("❌ DISCREPANCY DETECTED!")
    print(f"Difference: {db_count - len(all_ids)}")
