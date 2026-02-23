import toml, sys
sys.path.insert(0, '.')
from utils.flipdish_api import FlipDishAPI

secrets = toml.load('.streamlit/secrets.toml')
api = FlipDishAPI(secrets['flipdish']['bearer_token'], secrets['flipdish']['app_id'])

# Check ALL pages
page = 1
while True:
    orders, total = api.fetch_orders_page(page=page, limit=50)
    print(f"Page {page}: {len(orders)} orders, Total available: {total}")
    
    for o in orders:
        print(f"  → {o.get('OrderId')} | {o.get('PlacedTime')} | £{o.get('Amount')} | Status: {o.get('OrderState')}")
    
    if not orders or len(orders) < 50:
        break
    page += 1