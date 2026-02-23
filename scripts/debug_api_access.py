import os
import sys
from pathlib import Path
import toml
import sqlite3

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.flipdish_api import FlipDishAPI

def debug_api_access():
    secrets = toml.load(".streamlit/secrets.toml")
    token = secrets["flipdish"]["bearer_token"]
    app_id = secrets["flipdish"]["app_id"]
    
    api = FlipDishAPI(token, app_id)
    
    print("--- 🔍 STORE ACCESS AUDIT ---")
    stores = api.get_stores()
    print(f"Total stores found: {len(stores)}")
    for s in stores:
        print(f"Store: {s.get('Name')} | ID: {s.get('StoreId')} | Active: {s.get('IsActive')}")
    
    print("\n--- 📡 LATEST API RESPONSES ---")
    # Fetch page 1 and check the 'TotalRecordCount'
    orders, total = api.fetch_orders_page(page=1, limit=50)
    print(f"TotalRecordCount from API: {total}")
    print(f"Orders returned on page 1: {len(orders)}")
    
    if orders:
        print(f"Latest Order Time: {orders[0].get('PlacedTime')}")
        print(f"Oldest Order on Page 1: {orders[-1].get('PlacedTime')}")
        
    print("\n--- 🏛️ DATABASE SYNC CHECK ---")
    conn = sqlite3.connect('restaurant_data.db')
    latest_db = pd.read_sql_query("SELECT order_time FROM orders ORDER BY order_time DESC LIMIT 1", conn)
    print(f"Latest order in DB: {latest_db.iloc[0,0] if not latest_db.empty else 'NONE'}")
    conn.close()

if __name__ == "__main__":
    import pandas as pd
    debug_api_access()
