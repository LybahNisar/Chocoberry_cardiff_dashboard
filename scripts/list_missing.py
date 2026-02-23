import pandas as pd
import sqlite3

csv = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
conn = sqlite3.connect('restaurant_data.db')
db = pd.read_sql_query("SELECT order_id FROM orders", conn)
conn.close()

csv_ids = set(csv['Order ID'].astype(str))
db_ids = set(db['order_id'].astype(str))

missing = csv_ids - db_ids
if 'nan' in missing: missing.remove('nan')

print(f"Total missing (excluding nan): {len(missing)}")
for oid in sorted(list(missing)):
    print(f"MISSING_ID: {oid}")
