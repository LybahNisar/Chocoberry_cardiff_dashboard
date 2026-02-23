import toml
import sys
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))
from utils.flipdish_api import FlipDishAPI

def verify_all_api_data():
    secrets = toml.load(".streamlit/secrets.toml")
    token = secrets["flipdish"]["bearer_token"]
    app_id = secrets["flipdish"]["app_id"]
    
    api = FlipDishAPI(token, app_id)
    
    print("--- 🕵️ FULL API HISTORY SCAN ---")
    page = 1
    all_raw = []
    while True:
        orders, total = api.fetch_orders_page(page=page, limit=50)
        if not orders: break
        all_raw.extend(orders)
        if len(all_raw) >= total: break
        page += 1
    
    print(f"Total Unique Orders retrieved from API: {len(all_raw)}")
    
    if all_raw:
        df = pd.DataFrame([{
            'OrderId': o.get('OrderId'),
            'Time': o.get('PlacedTime'),
            'Store': o.get('Store', {}).get('Name'),
            'StoreId': o.get('Store', {}).get('StoreId'),
            'Total': o.get('Amount')
        } for o in all_raw])
        
        # Breakdown by date
        df['Date'] = pd.to_datetime(df['Time']).dt.date
        print("\nOrders per Day from API:")
        print(df.groupby('Date').size())
        
        print("\nStore Breakdown in API orders:")
        print(df.groupby('Store').size())
        
        print("\nSample of most recent API orders:")
        print(df.sort_values('Time', ascending=False).head(10).to_string(index=False))
    else:
        print("API returned zero orders.")

if __name__ == "__main__":
    verify_all_api_data()
