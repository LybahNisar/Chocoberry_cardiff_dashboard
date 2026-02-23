import toml, sys, requests
sys.path.insert(0, '.')
secrets = toml.load('.streamlit/secrets.toml')
token = secrets['flipdish']['bearer_token']
app_id = secrets['flipdish']['app_id']

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Try the sales summary endpoint that Flipdish portal uses
url = f"https://api.flipdish.co/api/v1.0/{app_id}/reports/salesummary"
response = requests.get(url, headers=headers, params={
    "startDate": "2026-02-17",
    "endDate": "2026-02-23"
})
print("Status code:", response.status_code)
print("Response:", response.text[:500])