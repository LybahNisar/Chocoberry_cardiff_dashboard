"""Full project audit - checks DB, API, and dashboard health"""
import sqlite3
import os
import sys

sys.path.insert(0, '.')

DB_PATH = 'restaurant_data.db'

def audit_database():
    print("=" * 60)
    print("AUDIT 1: DATABASE HEALTH")
    print("=" * 60)
    
    if not os.path.exists(DB_PATH):
        print("  FAIL: Database does not exist!")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Total orders
    c.execute("SELECT COUNT(*) FROM orders")
    total = c.fetchone()[0]
    print(f"  Total orders: {total}")
    
    # NULL dates
    c.execute("SELECT COUNT(*) FROM orders WHERE order_time IS NULL OR order_time = 'NaT'")
    null_dates = c.fetchone()[0]
    print(f"  Orders with NULL/NaT dates: {null_dates}")
    
    # Real date range
    c.execute("SELECT MIN(order_time), MAX(order_time) FROM orders WHERE order_time IS NOT NULL AND order_time != 'NaT'")
    dates = c.fetchone()
    print(f"  Date range: {dates[0]} to {dates[1]}")
    
    # Revenue
    c.execute("SELECT SUM(revenue), AVG(revenue) FROM orders")
    rev = c.fetchone()
    print(f"  Total revenue: {rev[0]:.2f}")
    print(f"  Avg revenue: {rev[1]:.2f}")
    
    # Duplicates
    c.execute("SELECT COUNT(*) FROM (SELECT order_id FROM orders GROUP BY order_id HAVING COUNT(*) > 1)")
    dupes = c.fetchone()[0]
    print(f"  Duplicate order IDs: {dupes}")
    
    # Dispatch types
    c.execute("SELECT dispatch_type, COUNT(*) FROM orders GROUP BY dispatch_type ORDER BY COUNT(*) DESC")
    print(f"  Dispatch types:")
    for row in c.fetchall():
        print(f"    {row[0]}: {row[1]}")
    
    # Payment methods
    c.execute("SELECT payment_method, COUNT(*) FROM orders GROUP BY payment_method ORDER BY COUNT(*) DESC")
    print(f"  Payment methods:")
    for row in c.fetchall():
        print(f"    {row[0]}: {row[1]}")
    
    # Order items
    c.execute("SELECT COUNT(*) FROM order_items")
    items = c.fetchone()[0]
    print(f"  Order items in DB: {items}")
    
    # Check if API orders are in DB
    c.execute("SELECT COUNT(*) FROM orders WHERE order_time > '2026-02-13'")
    api_orders = c.fetchone()[0]
    print(f"  Orders after Feb 13 (from API): {api_orders}")
    
    conn.close()
    return True

def audit_api():
    print("\n" + "=" * 60)
    print("AUDIT 2: API CONNECTION")
    print("=" * 60)
    
    # Load token
    token = ''
    app_id = ''
    try:
        with open('.streamlit/secrets.toml', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if 'bearer_token' in line and '=' in line:
                    token = line.split('=', 1)[1].strip().strip('"')
                if 'app_id' in line and '=' in line:
                    app_id = line.split('=', 1)[1].strip().strip('"')
    except:
        print("  FAIL: Cannot read secrets.toml")
        return False
    
    print(f"  Token: {'SET (' + str(len(token)) + ' chars)' if token else 'MISSING'}")
    print(f"  App ID: {app_id}")
    
    if not token or token == 'PASTE_YOUR_GENERATED_TOKEN_HERE':
        print("  FAIL: Token not configured")
        return False
    
    import requests
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    
    # Test stores
    try:
        r = requests.get(f'https://api.flipdish.co/api/v1.0/{app_id}/stores', headers=headers, timeout=15)
        print(f"  Stores endpoint: HTTP {r.status_code}")
        if r.status_code == 200:
            stores = r.json().get('Data', [])
            print(f"  Stores found: {len(stores)}")
            for s in stores:
                print(f"    - {s.get('Name')} (ID: {s.get('StoreId')})")
        elif r.status_code == 401:
            print("  FAIL: Token expired or invalid!")
            return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False
    
    # Test orders
    try:
        r = requests.get('https://api.flipdish.co/api/v1.0/orders', headers=headers, params={'page':1,'limit':5}, timeout=15)
        print(f"  Orders endpoint: HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            total = data.get('TotalRecordCount', 0)
            orders = data.get('Data', [])
            print(f"  API total orders: {total}")
            if orders:
                print(f"  Newest: {orders[0].get('PlacedTime')}")
                print(f"  Oldest: {orders[-1].get('PlacedTime')}")
    except Exception as e:
        print(f"  Orders FAIL: {e}")
    
    return True

def audit_dashboard():
    print("\n" + "=" * 60)
    print("AUDIT 3: DASHBOARD CODE")
    print("=" * 60)
    
    dash_path = 'dashboards/restaurant_dashboard.py'
    if not os.path.exists(dash_path):
        print("  FAIL: Dashboard file missing!")
        return False
    
    with open(dash_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    # Check critical features
    checks = {
        'FlipDishAPI import': 'from utils.flipdish_api import FlipDishAPI' in code,
        'SQLite loading': 'sqlite3' in code,
        'Sync button': 'Sync New Orders' in code,
        'DB path reference': 'restaurant_data.db' in code,
        'Date filter': 'Date Range' in code,
        'Dispatch filter': 'Dispatch' in code,
        'Revenue metrics': 'Revenue' in code,
        'Menu analysis': 'show_menu_analysis' in code,
        'Password protection': 'check_password' in code,
        'Cache decorator': 'cache_data' in code,
    }
    
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {check}")
    
    return all(checks.values())

def audit_files():
    print("\n" + "=" * 60)
    print("AUDIT 4: PROJECT FILES")
    print("=" * 60)
    
    critical_files = {
        '.streamlit/secrets.toml': 'API credentials',
        'dashboards/restaurant_dashboard.py': 'Main dashboard',
        'dashboards/menu_analysis.py': 'Menu analysis module',
        'utils/__init__.py': 'Utils package',
        'utils/flipdish_api.py': 'API client',
        'scripts/setup_database.py': 'DB setup script',
        'scripts/import_history.py': 'History import tool',
        'restaurant_data.db': 'SQLite database',
        'requirements.txt': 'Python dependencies',
    }
    
    for path, desc in critical_files.items():
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        status = "PASS" if exists else "FAIL"
        print(f"  [{status}] {path} ({desc}) - {size:,} bytes")

def audit_sync():
    print("\n" + "=" * 60)
    print("AUDIT 5: SYNC TEST (API -> DB)")
    print("=" * 60)
    
    # Load token
    token = ''
    app_id = ''
    try:
        with open('.streamlit/secrets.toml', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if 'bearer_token' in line and '=' in line:
                    token = line.split('=', 1)[1].strip().strip('"')
                if 'app_id' in line and '=' in line:
                    app_id = line.split('=', 1)[1].strip().strip('"')
    except:
        print("  Cannot read secrets")
        return
    
    if not token or token == 'PASTE_YOUR_GENERATED_TOKEN_HERE':
        print("  Token not set, skipping sync test")
        return
    
    from utils.flipdish_api import FlipDishAPI
    api = FlipDishAPI(token, app_id)
    
    # Count before
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM orders")
    before = c.fetchone()[0]
    conn.close()
    
    # Run sync
    added = api.sync_to_db(DB_PATH)
    
    # Count after
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM orders")
    after = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM orders WHERE order_time > '2026-02-13'")
    api_orders = c.fetchone()[0]
    conn.close()
    
    print(f"  Orders before sync: {before}")
    print(f"  Orders after sync:  {after}")
    print(f"  New orders added:   {added}")
    print(f"  Total API orders (after Feb 13): {api_orders}")

if __name__ == '__main__':
    print("COMPREHENSIVE PROJECT AUDIT")
    print("Date: 2026-02-19")
    print()
    
    audit_files()
    db_ok = audit_database()
    api_ok = audit_api()
    dash_ok = audit_dashboard()
    
    if db_ok and api_ok:
        audit_sync()
    
    print("\n" + "=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    print(f"  Database:  {'PASS' if db_ok else 'FAIL'}")
    print(f"  API:       {'PASS' if api_ok else 'FAIL'}")
    print(f"  Dashboard: {'PASS' if dash_ok else 'FAIL'}")
    print("=" * 60)
