"""Concise accuracy check with numbered lines"""
import sqlite3, pandas as pd
from pathlib import Path

# CSV
csv = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
csv['Order time'] = pd.to_datetime(csv['Order time'])
for col in ['Revenue','Gross sales','Tax on gross sales','Tips','Delivery charges']:
    if col in csv.columns:
        if csv[col].dtype == 'object':
            csv[col] = csv[col].str.replace(',','',regex=False)
        csv[col] = pd.to_numeric(csv[col], errors='coerce').fillna(0)

# DB
conn = sqlite3.connect('restaurant_data.db')
db = pd.read_sql_query("SELECT * FROM orders WHERE order_time IS NOT NULL AND order_time != 'NaT'", conn)
db['order_time'] = pd.to_datetime(db['order_time'], format='mixed')
conn.close()

csv_era = db[db['order_time'] <= '2026-02-13']
api_era = db[db['order_time'] > '2026-02-13']

# Print line by line
results = []
results.append(f"CSV_ORDERS={len(csv)}")
results.append(f"CSV_REVENUE={csv['Revenue'].sum():.2f}")
results.append(f"CSV_DATE={csv['Order time'].min()} to {csv['Order time'].max()}")
results.append(f"DB_TOTAL={len(db)}")
results.append(f"DB_CSV_ERA={len(csv_era)}")
results.append(f"DB_API_ERA={len(api_era)}")
results.append(f"DB_REVENUE={db['revenue'].sum():.2f}")
results.append(f"DB_DATE={db['order_time'].min()} to {db['order_time'].max()}")

# Missing orders
csv_ids = set(csv['Order ID'].astype(str))
db_ids = set(csv_era['order_id'].astype(str))
missing = csv_ids - db_ids
results.append(f"MISSING_FROM_DB={len(missing)}")

# Revenue comparison
csv_rev = csv['Revenue'].sum()
db_csv_rev = csv_era['revenue'].sum()
results.append(f"CSV_REV={csv_rev:.2f}")
results.append(f"DB_CSV_REV={db_csv_rev:.2f}")
results.append(f"REV_DIFF={abs(csv_rev - db_csv_rev):.2f}")

# API details
if len(api_era) > 0:
    results.append(f"API_REV={api_era['revenue'].sum():.2f}")
    results.append(f"API_AVG={api_era['revenue'].mean():.2f}")

# Expected dashboard values
results.append(f"DASH_ORDERS={len(db)}")
results.append(f"DASH_REVENUE={db['revenue'].sum():.2f}")
results.append(f"DASH_AVG={db['revenue'].mean():.2f}")
results.append(f"DASH_TAX={db['tax'].sum():.2f}")
results.append(f"DASH_DELIVERY={db['delivery_charges'].sum():.2f}")

for r in results:
    print(r)
