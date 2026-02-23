import os
import sqlite3
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.flipdish_api import FlipDishAPI
import toml

# Load secrets
secrets = toml.load(".streamlit/secrets.toml")
token = secrets["flipdish"]["bearer_token"]
app_id = secrets["flipdish"]["app_id"]

api = FlipDishAPI(token, app_id)

print("--- API FETCH AUDIT ---")
page = 1
total_orders_available = 0
all_api_orders = []

while True:
    orders, total = api.fetch_orders_page(page=page, limit=50)
    if not orders:
        break
    all_api_orders.extend(orders)
    total_orders_available = total
    print(f"Page {page}: Fetched {len(orders)} orders (Total available: {total})")
    if len(all_api_orders) >= total:
        break
    page += 1

print(f"\nTotal orders found in API window: {len(all_api_orders)}")
if all_api_orders:
    print(f"Date Range in API: {all_api_orders[-1].get('PlacedTime')} to {all_api_orders[0].get('PlacedTime')}")

# Check DB
conn = sqlite3.connect('restaurant_data.db')
db_count = pd.read_sql_query("SELECT COUNT(*) as count FROM orders", conn).iloc[0]['count']
api_era_count = pd.read_sql_query("SELECT COUNT(*) as count FROM orders WHERE order_time > '2026-02-13'", conn).iloc[0]['count']
conn.close()

print(f"\n--- DATABASE STATUS ---")
print(f"Total orders in DB: {db_count}")
print(f"Orders from API era (post-Feb 13): {api_era_count}")

# Check for any missing from API era
api_ids_in_window = set(str(o.get('OrderId')) for o in all_api_orders)
conn = sqlite3.connect('restaurant_data.db')
db_ids = set(pd.read_sql_query("SELECT order_id FROM orders", conn)['order_id'].astype(str))
conn.close()

missing_from_db = api_ids_in_window - db_ids
print(f"API Orders Missing from DB: {len(missing_from_db)}")
if missing_from_db:
    print(f"Missing IDs: {missing_from_db}")
