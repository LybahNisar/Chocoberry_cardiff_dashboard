"""
Flipdish API Connection Test (Bearer Token)
=============================================
Tests your API connection using the bearer token from Flipdish portal.

Usage:
    py scripts/test_flipdish_api.py
"""

import sys
import os
import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_secrets():
    """Load secrets from .streamlit/secrets.toml"""
    secrets_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '.streamlit', 'secrets.toml'
    )
    
    secrets = {}
    current_section = None
    
    with open(secrets_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('['):
                current_section = line.strip('[]')
                secrets[current_section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')
                if current_section:
                    secrets[current_section][key] = value
                else:
                    secrets[key] = value
    
    return secrets


def main():
    print("=" * 60)
    print("FLIPDISH API CONNECTION TEST")
    print("=" * 60)
    
    # Load credentials
    print("\n[1/4] Loading credentials...")
    secrets = load_secrets()
    
    flipdish = secrets.get('flipdish', {})
    app_id = flipdish.get('app_id', '')
    bearer_token = flipdish.get('bearer_token', '')
    
    print(f"  App ID: {app_id}")
    print(f"  Token:  {'SET (' + str(len(bearer_token)) + ' chars)' if bearer_token and bearer_token != 'PASTE_YOUR_GENERATED_TOKEN_HERE' else 'NOT SET'}")
    
    if not bearer_token or bearer_token == 'PASTE_YOUR_GENERATED_TOKEN_HERE':
        print("\n  ERROR: Add your bearer token to .streamlit/secrets.toml")
        return
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
    }
    
    BASE = "https://api.flipdish.co"
    
    # Test 1: Stores
    print(f"\n[2/4] Testing API connection...")
    try:
        r = requests.get(f"{BASE}/api/v1.0/{app_id}/stores", headers=headers, timeout=15)
        print(f"  Stores endpoint: HTTP {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            stores = data.get('Data', data) if isinstance(data, dict) else data
            if isinstance(stores, list):
                print(f"  Found {len(stores)} store(s)")
                for s in stores[:5]:
                    if isinstance(s, dict):
                        print(f"    - {s.get('Name', s.get('StoreName', 'Unknown'))} (ID: {s.get('StoreId', s.get('Id', '?'))})")
            else:
                print(f"  Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                print(f"  Preview: {str(data)[:300]}")
        elif r.status_code == 401:
            print("  FAILED: Token is invalid or expired")
            print(f"  Response: {r.text[:200]}")
            return
        else:
            print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 2: Orders
    print(f"\n[3/4] Fetching orders...")
    
    endpoints_to_try = [
        f"/api/v1.0/{app_id}/orders",
        f"/api/v1.0/orders",
        f"/reporting/v1.0/{app_id}/order/list",
        f"/reporting/v1.0/{app_id}/order/overview",
    ]
    
    working_endpoint = None
    order_fields = []
    
    for endpoint in endpoints_to_try:
        try:
            url = f"{BASE}{endpoint}"
            r = requests.get(url, headers=headers, params={"page": 1, "limit": 3}, timeout=15)
            print(f"\n  {endpoint}")
            print(f"    Status: {r.status_code}")
            
            if r.status_code == 200:
                data = r.json()
                working_endpoint = endpoint
                
                if isinstance(data, dict):
                    print(f"    Keys: {list(data.keys())}")
                    
                    # Find the orders list
                    orders = data.get('Data', data.get('Orders', data.get('orders', [])))
                    
                    if isinstance(orders, list) and orders:
                        print(f"    Found {len(orders)} orders!")
                        print(f"\n    --- SAMPLE ORDER FIELDS ---")
                        sample = orders[0]
                        order_fields = list(sample.keys())
                        for key in sorted(sample.keys()):
                            val = sample[key]
                            if isinstance(val, (dict, list)):
                                val = f"[{type(val).__name__} with {len(val)} items]"
                            elif isinstance(val, str) and len(val) > 60:
                                val = val[:60] + "..."
                            print(f"      {key}: {val}")
                        
                        # Check for nested order items
                        if 'OrderItems' in sample or 'Items' in sample or 'OrderLines' in sample:
                            items_key = 'OrderItems' if 'OrderItems' in sample else ('Items' if 'Items' in sample else 'OrderLines')
                            items = sample[items_key]
                            if isinstance(items, list) and items:
                                print(f"\n    --- ORDER ITEMS ({len(items)} items) ---")
                                for key in sorted(items[0].keys()):
                                    print(f"      {key}: {items[0][key]}")
                        
                        break  # Found working endpoint
                    elif isinstance(orders, dict):
                        print(f"    Data keys: {list(orders.keys())}")
                        print(f"    Preview: {str(orders)[:300]}")
                elif isinstance(data, list) and data:
                    print(f"    Found {len(data)} orders!")
                    working_endpoint = endpoint
                    order_fields = list(data[0].keys())
                    for key in sorted(data[0].keys()):
                        print(f"      {key}: {data[0][key]}")
                    break
            elif r.status_code != 404:
                print(f"    Body: {r.text[:150]}")
                
        except Exception as e:
            print(f"    Error: {e}")
    
    # Summary
    print("\n\n[4/4] RESULTS")
    print("=" * 60)
    
    if working_endpoint:
        print(f"  Authentication:    PASSED")
        print(f"  Working endpoint:  {working_endpoint}")
        print(f"  Order fields:      {len(order_fields)}")
        print(f"\n  Ready to integrate with dashboard!")
        print(f"\n  API fields found:")
        for f in order_fields:
            print(f"    - {f}")
    else:
        print(f"  Authentication:    {'PASSED' if r.status_code != 401 else 'FAILED'}")
        print(f"  Orders endpoint:   NOT FOUND")
        print(f"\n  The token works but we need to find the right endpoint.")
        print(f"  Check Flipdish API docs for the correct orders URL.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
