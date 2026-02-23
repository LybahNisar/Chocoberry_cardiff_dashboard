import toml, sys, requests
sys.path.insert(0, '.')
secrets = toml.load('.streamlit/secrets.toml')
token = secrets['flipdish']['bearer_token']

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Try fetching with different order states
for state in ["Created", "Accepted", "Dispatched", "ReadyToProcess"]:
    url = "https://api.flipdish.co/api/v1.0/orders"
    response = requests.get(url, headers=headers, params={
        "page": 1, 
        "limit": 50,
        "orderState": state
    })
    data = response.json()
    total = data.get("TotalRecordCount", 0)
    print(f"Status '{state}': {total} orders found")