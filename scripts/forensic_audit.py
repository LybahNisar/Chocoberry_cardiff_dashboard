import pandas as pd
import sqlite3

# Load CSV with NO cleaning/parsing first
print("--- RAW CSV ANALYSIS ---")
csv_raw = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
print(f"Total rows in CSV: {len(csv_raw)}")

# Check for specific high revenue rows
csv_raw['Revenue_num'] = pd.to_numeric(csv_raw['Revenue'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
top_5 = csv_raw.nlargest(5, 'Revenue_num')
print("\nTop 5 Revenue Rows in CSV:")
for _, row in top_5.iterrows():
    print(f"ID: {row['Order ID']}, Time: {row['Order time']}, Revenue: {row['Revenue']}")

# Check for rows where Order ID is missing or NaN
nan_id_rows = csv_raw[csv_raw['Order ID'].isna()]
print(f"\nRows with NaN Order ID: {len(nan_id_rows)}")
if len(nan_id_rows) > 0:
    print(f"Revenue from NaN ID rows: {nan_id_rows['Revenue_num'].sum():.2f}")

# Database Check
conn = sqlite3.connect('restaurant_data.db')
db_orders = pd.read_sql_query("SELECT order_id FROM orders", conn)
conn.close()

# Identify the 19 missing IDs
# We need to be careful with ID types
csv_ids = set(csv_raw['Order ID'].astype(str).unique())
db_ids = set(db_orders['order_id'].astype(str).unique())

missing_from_db = csv_ids - db_ids
print(f"\nMissing IDs from DB: {len(missing_from_db)}")
if 'nan' in missing_from_db:
    missing_from_db.remove('nan')
    print(" (Note: 'nan' removed from the 19 count for detail view)")

print("\nSample of Missing IDs (the 19):")
count = 0
for oid in sorted(list(missing_from_db)):
    if count >= 20: break
    row = csv_raw[csv_raw['Order ID'].astype(str) == oid].iloc[0]
    print(f"ID: {oid}, Time: {row['Order time']}, Revenue: {row['Revenue']}")
    count += 1
