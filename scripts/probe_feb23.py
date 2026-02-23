import toml
import requests
from datetime import datetime, timedelta

secrets = toml.load(".streamlit/secrets.toml")
token   = secrets["flipdish"]["bearer_token"]
app_id  = secrets["flipdish"]["app_id"]

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
BASE    = "https://api.flipdish.co"

print(f"Checking API on: {datetime.now()}")

# Get stores first
stores_r = requests.get(f"{BASE}/api/v1.0/{app_id}/stores", headers=headers, timeout=15)
store_ids = []
if stores_r.status_code == 200:
    data = stores_r.json().get("Data", [])
    for s in data:
        print(f"Store: {s.get('Name')} | StoreId: {s.get('StoreId')}")
        store_ids.append(s.get("StoreId"))

# Check global orders
r = requests.get(f"{BASE}/api/v1.0/orders?limit=100", headers=headers, timeout=15)
if r.status_code == 200:
    data = r.json()
    orders = data.get("Data", [])
    print(f"\nGlobal /orders | Total: {data.get('TotalRecordCount')} | Returned: {len(orders)}")
    if orders:
        times = [o.get('PlacedTime') for o in orders]
        times.sort()
        print(f"Range: {times[0]} to {times[-1]}")
else:
    print(f"Error fetching global orders: {r.status_code} {r.text}")

# Check specific stores
for sid in store_ids:
    r = requests.get(f"{BASE}/api/v1.0/orders?storeId={sid}&limit=100", headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        orders = data.get("Data", [])
        print(f"\nStore {sid} orders | Total: {data.get('TotalRecordCount')} | Returned: {len(orders)}")
        if orders:
            times = [o.get('PlacedTime') for o in orders]
            times.sort()
            print(f"Range: {times[0]} to {times[-1]}")
    else:
        print(f"Error fetching store {sid} orders: {r.status_code} {r.text}")
