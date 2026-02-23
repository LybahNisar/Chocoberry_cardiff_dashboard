import sqlite3
import os
import sys
sys.path.insert(0, '.')

DB = 'restaurant_data.db'

print('=== DATABASE HEALTH ===')
conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM orders')
print('Total orders:', c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM orders WHERE order_time IS NULL OR order_time = 'NaT'")
print('Null/NaT dates:', c.fetchone()[0])

c.execute("SELECT MIN(order_time) FROM orders WHERE order_time IS NOT NULL AND order_time != 'NaT'")
print('Earliest:', c.fetchone()[0])

c.execute("SELECT MAX(order_time) FROM orders WHERE order_time IS NOT NULL AND order_time != 'NaT'")
print('Latest:', c.fetchone()[0])

c.execute('SELECT SUM(revenue) FROM orders')
print('Total revenue:', c.fetchone()[0])

c.execute('SELECT COUNT(*) FROM order_items')
print('Item records:', c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM orders WHERE order_time > '2026-02-13'")
print('API orders (post Feb13):', c.fetchone()[0])

c.execute('SELECT dispatch_type, COUNT(*) FROM orders GROUP BY dispatch_type')
for r in c.fetchall():
    print('  Dispatch:', r[0], '=', r[1])

c.execute('SELECT payment_method, COUNT(*) FROM orders GROUP BY payment_method')
for r in c.fetchall():
    print('  Payment:', r[0], '=', r[1])

conn.close()

print()
print('=== API CHECK ===')
token = ''
app_id = ''
with open('.streamlit/secrets.toml', encoding='utf-8', errors='ignore') as f:
    for line in f:
        line = line.strip()
        if 'bearer_token' in line and '=' in line:
            token = line.split('=', 1)[1].strip().strip('"')
        if 'app_id' in line and '=' in line:
            app_id = line.split('=', 1)[1].strip().strip('"')

print('Token:', len(token), 'chars')
print('App ID:', app_id)

import requests
headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}
r = requests.get('https://api.flipdish.co/api/v1.0/orders', headers=headers, params={'page': 1, 'limit': 5}, timeout=15)
print('API Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('API Total Orders:', data.get('TotalRecordCount'))
    orders = data.get('Data', [])
    if orders:
        print('Newest:', orders[0].get('PlacedTime'))
        print('Oldest:', orders[-1].get('PlacedTime'))

print()
print('=== SYNC TEST ===')
from utils.flipdish_api import FlipDishAPI
api = FlipDishAPI(token, app_id)

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM orders')
before = c.fetchone()[0]
conn.close()

added = api.sync_to_db(DB)

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM orders')
after = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM orders WHERE order_time > '2026-02-13'")
api_orders = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM order_items")
items_after = c.fetchone()[0]
conn.close()

print('Before sync:', before)
print('After sync:', after)
print('New added:', added)
print('Post-Feb13 orders:', api_orders)
print('Item records after:', items_after)

print()
print('=== DASHBOARD CODE CHECK ===')
with open('dashboards/restaurant_dashboard.py', encoding='utf-8', errors='ignore') as f:
    code = f.read()

checks = [
    ('FlipDishAPI import', 'from utils.flipdish_api import FlipDishAPI'),
    ('SQLite loading', 'sqlite3'),
    ('Sync button', 'Sync New Orders'),
    ('DB path', 'restaurant_data.db'),
    ('Date filter', 'Date Range'),
    ('Dispatch filter', 'Dispatch'),
    ('Revenue', 'Revenue'),
    ('Menu analysis', 'show_menu_analysis'),
    ('Password', 'check_password'),
    ('Cache', 'cache_data'),
]

for name, pattern in checks:
    status = 'PASS' if pattern in code else 'FAIL'
    print(f'  [{status}] {name}')

print()
print('=== DONE ===')
