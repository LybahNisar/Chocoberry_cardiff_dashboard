import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def run_forensic_audit():
    conn = sqlite3.connect('restaurant_data.db')
    
    # 1. Timeline Gap Analysis
    print("--- 📅 TIMELINE CONTINUITY CHECK ---")
    query = """
    SELECT 
        DATE(order_time) as date, 
        COUNT(*) as order_count, 
        SUM(revenue) as daily_revenue
    FROM orders
    WHERE order_time >= '2026-02-01'
    GROUP BY DATE(order_time)
    ORDER BY date
    """
    timeline = pd.read_sql_query(query, conn)
    print(timeline.to_string(index=False))
    
    # 2. Check for "Dead Hours" in the last 3 days
    print("\n--- 🕐 HOURLY GAP ANALYSIS (Last 3 Days) ---")
    query_hours = """
    SELECT 
        DATE(order_time) as date,
        strftime('%H', order_time) as hour,
        COUNT(*) as count
    FROM orders
    WHERE order_time >= DATE('now', '-3 days')
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    hourly = pd.read_sql_query(query_hours, conn)
    print(hourly.to_string(index=False))

    # 3. CSV vs API Transition Detail
    print("\n--- 🔗 CSV-TO-API HANDOFF DETAIL ---")
    # Last few CSV orders
    csv_end = pd.read_sql_query("SELECT order_id, order_time, revenue FROM orders WHERE order_time <= '2026-02-13 12:00:00' ORDER BY order_time DESC LIMIT 3", conn)
    print("Last CSV Era Orders:")
    print(csv_end.to_string(index=False))
    
    # First few API orders
    api_start = pd.read_sql_query("SELECT order_id, order_time, revenue FROM orders WHERE order_time > '2026-02-13 12:00:00' ORDER BY order_time ASC LIMIT 3", conn)
    print("\nFirst API Era Orders:")
    print(api_start.to_string(index=False))

    conn.close()

if __name__ == "__main__":
    run_forensic_audit()
