"""
Test Flipdish API with different filter parameters to get all orders.
"""
import toml
import requests
from datetime import datetime, timedelta

secrets = toml.load(".streamlit/secrets.toml")
token   = secrets["flipdish"]["bearer_token"]
app_id  = secrets["flipdish"]["app_id"]

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
BASE    = "https://api.flipdish.co"

def test(label, url, params=None):
    r = requests.get(url, headers=headers, params=params, timeout=15)
    if r.status_code == 200:
        data = r.json()
        total   = data.get("TotalRecordCount", "?")
        records = len(data.get("Data", []))
        print(f"[{r.status_code}] {label}")
        print(f"       TotalRecordCount={total}  |  rows returned={records}")
        if records > 0:
            d = data["Data"][0]
            print(f"       Sample OrderId={d.get('OrderId')}  Time={d.get('PlacedTime')}")
    else:
        print(f"[{r.status_code}] {label}")
        print(f"       Error: {r.text[:100]}")
    print()

# First get the store ID
stores_r = requests.get(f"{BASE}/api/v1.0/{app_id}/stores", headers=headers, timeout=15)
store_ids = []
if stores_r.status_code == 200:
    stores = stores_r.json().get("Data", [])
    for s in stores:
        print(f"Found Store: {s.get('Name')}  StoreId={s.get('StoreId')}")
        store_ids.append(s.get("StoreId"))
print()

# Basic
test("Basic /orders", f"{BASE}/api/v1.0/orders")

# With limit=100
test("With limit=100", f"{BASE}/api/v1.0/orders", {"limit": 100})

# With storeId filter for each discovered store
for sid in store_ids:
    test(f"With storeId={sid}", f"{BASE}/api/v1.0/orders", {"storeId": sid, "limit": 100})

# With date range (last 30 days)
start = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S")
end   = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
test(f"With date range (last 30 days)", f"{BASE}/api/v1.0/orders",
     {"start": start, "end": end, "limit": 100})

# Physical restaurant orders endpoint
test("physicalRestaurantId filter", f"{BASE}/api/v1.0/orders",
     {"physicalRestaurantId": store_ids[0] if store_ids else 72, "limit": 100})

# Try different order status filters
for status in ["ReadyToProcess", "AcceptedByRestaurant", "Dispatched"]:
    test(f"OrderState={status}", f"{BASE}/api/v1.0/orders",
         {"orderState": status, "limit": 100})
