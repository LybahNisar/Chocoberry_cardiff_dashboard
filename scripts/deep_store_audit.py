import toml
import sys
import sqlite3
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))
from utils.flipdish_api import FlipDishAPI

def deep_store_audit():
    secrets = toml.load(".streamlit/secrets.toml")
    token = secrets["flipdish"]["bearer_token"]
    app_id = secrets["flipdish"]["app_id"]
    
    api = FlipDishAPI(token, app_id)
    
    print("--- 🔍 STORE AUDIT ---")
    stores = api.get_stores()
    for s in stores:
        print(f"STORE: {s.get('Name')} | ID: {s.get('StoreId')} | APP: {s.get('AppId')}")
    
    print("\n--- 📡 RECENT ORDERS (ALL STORES) ---")
    orders, total = api.fetch_orders_page(page=1, limit=100)
    print(f"Total API records found in recent window: {total}")
    
    if orders:
        df_api = pd.DataFrame([
            {
                'id': o.get('OrderId'),
                'time': o.get('PlacedTime'),
                'store': o.get('Store', {}).get('Name'),
                'store_id': o.get('Store', {}).get('StoreId'),
                'revenue': o.get('Amount')
            } for o in orders
        ])
        print(df_api.to_string(index=False))
        
        # Count by store
        print("\nOrders per Store ID in API response:")
        print(df_api['store_id'].value_counts())
    else:
        print("No orders returned from API.")

    print("\n--- 🏛️ CSV HISTORY SAMPLE ---")
    conn = sqlite3.connect('restaurant_data.db')
    # Let's get a few from the CSV era
    csv_sample = pd.read_sql_query("SELECT property_name, COUNT(*) as count FROM orders WHERE order_time < '2026-02-13' GROUP BY 1", conn)
    print("Store names in CSV History:")
    print(csv_sample)
    conn.close()

if __name__ == "__main__":
    deep_store_audit()
