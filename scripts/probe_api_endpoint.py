"""
Probe all possible Flipdish API endpoints to find where the live orders actually are.
"""
import sys
import toml
import requests
from pathlib import Path

secrets = toml.load(".streamlit/secrets.toml")
token   = secrets["flipdish"]["bearer_token"]
app_id  = secrets["flipdish"]["app_id"]

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

endpoints = [
    f"/api/v1.0/orders",
    f"/api/v1.0/{app_id}/orders",
    f"/api/v1.0/orders?limit=20",
    f"/api/v1.0/{app_id}/orders?limit=20",
]

print(f"App ID: {app_id}")
print(f"Token (first 20 chars): {token[:20]}...\n")

for path in endpoints:
    url = f"https://api.flipdish.co{path}"
    r = requests.get(url, headers=headers, timeout=15)
    data = {}
    try:
        data = r.json()
    except:
        pass
    total = data.get("TotalRecordCount", "N/A") if isinstance(data, dict) else "PARSE_ERR"
    results = len(data.get("Data", [])) if isinstance(data, dict) else 0
    print(f"Status {r.status_code} | TotalRecordCount={total} | Data rows={results}")
    print(f"  URL: {url}")
    if r.status_code != 200:
        print(f"  Error: {r.text[:200]}")
    print()
