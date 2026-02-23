"""
Deep API test - try ALL Flipdish endpoints to find historical data
"""
import requests
import json

# Load token
token = ''
with open('.streamlit/secrets.toml') as f:
    for line in f:
        if 'bearer_token' in line and '=' in line:
            token = line.split('=', 1)[1].strip().strip('"')

headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
BASE = 'https://api.flipdish.co'

print("=" * 60)
print("DEEP API TEST - Finding ALL Orders")
print("=" * 60)

# Test 1: Orders with different state filters
print("\n--- TEST 1: Orders with state filters ---")
states = ['', 'AcceptedByRestaurant', 'ReadyForPickup', 'Dispatched', 'Delivered', 'PlacedCanBeCancelled']
for state in states:
    params = {'page': 1, 'limit': 1}
    if state:
        params['orderStates'] = state
    try:
        r = requests.get(f'{BASE}/api/v1.0/orders', headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            d = r.json()
            print(f"  State='{state}': Total={d.get('TotalRecordCount', '?')}")
        else:
            print(f"  State='{state}': HTTP {r.status_code}")
    except Exception as e:
        print(f"  State='{state}': Error - {e}")

# Test 2: Try with appId in URL
print("\n--- TEST 2: App-specific order endpoints ---")
app_endpoints = [
    '/api/v1.0/br1153/orders',
    '/api/v1.0/br1153/orders/summary',
]
for ep in app_endpoints:
    try:
        r = requests.get(f'{BASE}{ep}', headers=headers, params={'page':1,'limit':1}, timeout=15)
        print(f"  {ep}: HTTP {r.status_code}")
        if r.status_code == 200:
            d = r.json()
            print(f"    Keys: {list(d.keys())[:5]}")
            print(f"    Total: {d.get('TotalRecordCount', '?')}")
    except Exception as e:
        print(f"  {ep}: Error - {e}")

# Test 3: Reporting API (the one that should have history)
print("\n--- TEST 3: Reporting API (Historical Data) ---")
report_endpoints = [
    '/reporting/v1.0/br1153/order/list',
    '/reporting/v1.0/br1153/order/overview',
    '/reporting/v1.0/br1153/order/store',
    '/reporting/v1.0/br1153/order/platform',
    '/reporting/v1.0/br1153/order/deliverytype',
]
for ep in report_endpoints:
    try:
        params = {
            'page': 1,
            'limit': 5,
            'startDate': '2025-01-01',
            'endDate': '2026-02-18',
        }
        r = requests.get(f'{BASE}{ep}', headers=headers, params=params, timeout=20)
        print(f"  {ep}")
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            d = r.json()
            if isinstance(d, dict):
                print(f"    Keys: {list(d.keys())[:8]}")
                total = d.get('TotalRecordCount', d.get('Count', d.get('TotalCount', '?')))
                print(f"    Total: {total}")
                data = d.get('Data', d.get('data', d.get('Orders', [])))
                if isinstance(data, list) and data:
                    print(f"    Records: {len(data)}")
                    if isinstance(data[0], dict):
                        print(f"    Sample keys: {list(data[0].keys())[:8]}")
            elif isinstance(d, list):
                print(f"    Records: {len(d)}")
        elif r.status_code != 404:
            print(f"    Body: {r.text[:150]}")
    except requests.exceptions.Timeout:
        print(f"    TIMEOUT (20s)")
    except Exception as e:
        print(f"    Error: {e}")

# Test 4: CSV download endpoint
print("\n--- TEST 4: CSV Download API ---")
csv_endpoints = [
    '/reporting/v1.0/br1153/csv/sales',
    '/reporting/v1.0/br1153/csv/orders',
]
for ep in csv_endpoints:
    try:
        r = requests.get(f'{BASE}{ep}', headers=headers, params={'startDate':'2025-01-01','endDate':'2026-02-18'}, timeout=20, allow_redirects=False)
        print(f"  {ep}: HTTP {r.status_code}")
        if r.status_code in [200, 301, 302]:
            print(f"    Headers: {dict(r.headers)}")
    except requests.exceptions.Timeout:
        print(f"  {ep}: TIMEOUT")
    except Exception as e:
        print(f"  {ep}: Error - {e}")

# Test 5: Store-specific orders
print("\n--- TEST 5: Store-specific orders ---")
store_ids = [72495, 73684]
for sid in store_ids:
    try:
        r = requests.get(f'{BASE}/api/v1.0/orders', headers=headers, 
                        params={'page':1,'limit':1,'storeId':sid}, timeout=15)
        if r.status_code == 200:
            d = r.json()
            print(f"  Store {sid}: Total={d.get('TotalRecordCount','?')}")
    except Exception as e:
        print(f"  Store {sid}: Error - {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
