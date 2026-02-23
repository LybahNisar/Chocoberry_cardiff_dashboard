import sqlite3
import pandas as pd
from pathlib import Path

# Set the path to your database
# Using absolute path to ensure it works regardless of where the script is run from
db_path = Path('C:/Users/GEO/Desktop/Dashboard/restaurant_data.db')

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(str(db_path))
        
        print("\n" + "="*40)
        print("📊 DATABASE SUMMARY REPORT")
        print("="*40)
        
        # 1. Check Tables
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
        print(f"\n📁 Tables in Database: {', '.join(tables['name'].tolist())}")
        
        # 2. Summary of Orders
        orders_summary = pd.read_sql_query("SELECT COUNT(*) as total, MIN(order_time) as start, MAX(order_time) as end FROM orders", conn)
        print(f"\n📈 Orders Table Status:")
        print(f"   - Total Record Count: {orders_summary.iloc[0]['total']:,}")
        print(f"   - Coverage Start:    {orders_summary.iloc[0]['start']}")
        print(f"   - Coverage End:      {orders_summary.iloc[0]['end']}")
        
        # 3. API-Era Breakdown (Post Feb 13)
        api_era = pd.read_sql_query("SELECT COUNT(*) as count, SUM(revenue) as rev FROM orders WHERE order_time > '2026-02-13'", conn)
        print(f"\n📡 Live API Data (Synced Feb 14-18):")
        print(f"   - Total API Orders:  {api_era.iloc[0]['count']}")
        print(f"   - Total API Revenue: £{api_era.iloc[0]['rev']:.2f}")

        # 4. View Most Recent 20 Orders (Full Sample)
        print("\n🕒 RECENT ORDERS PREVIEW (Last 20):")
        recent = pd.read_sql_query("""
            SELECT 
                order_id as 'Order ID', 
                order_time as 'Time', 
                revenue as 'Revenue (£)', 
                dispatch_type as 'Type' 
            FROM orders 
            ORDER BY order_time DESC 
            LIMIT 20
        """, conn)
        print(recent.to_string(index=False))
        
        # 4. Item Records
        items_count = pd.read_sql_query("SELECT COUNT(*) as total FROM order_items", conn)
        print(f"\n📦 Item Details Records: {items_count.iloc[0]['total']:,}")
        
        print("\n" + "="*40)
        print("✅ End of Report")
        print("="*40)
        
        conn.close()
    except Exception as e:
        print(f"❌ Error reading database: {e}")
