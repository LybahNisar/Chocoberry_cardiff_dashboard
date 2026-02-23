import toml, sys, requests
sys.path.insert(0, '.')
secrets = toml.load('.streamlit/secrets.toml')
token = secrets['flipdish']['bearer_token']
app_id = secrets['flipdish']['app_id']

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Try different known Flipdish endpoints
endpoints = [
    f"/api/v1.0/{app_id}/orders",
    f"/api/v1.0/orders?appId={app_id}",
    f"/api/v1.0/{app_id}/sales",
    f"/api/v1.0/{app_id}/analytics/ordersummary",
    f"/api/v1.0/{app_id}/reports/ordersummary",
    f"/api/v1.0/{app_id}/orderstatistics",
]

for endpoint in endpoints:
    url = f"https://api.flipdish.co{endpoint}"
    response = requests.get(url, headers=headers, params={
        "start": "2026-02-22",
        "end": "2026-02-23"
    })
    print(f"{response.status_code} → {endpoint}")
    if response.status_code == 200:
        print(f"   FOUND! Response: {response.text[:200]}")