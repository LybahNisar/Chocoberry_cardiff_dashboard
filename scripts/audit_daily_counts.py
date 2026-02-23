import sqlite3
import pandas as pd

def audit_daily_counts():
    conn = sqlite3.connect('restaurant_data.db')
    
    print("--- 📉 DAILY ORDER COUNT AUDIT ---")
    query = """
    SELECT 
        DATE(order_time) as order_date,
        COUNT(*) as order_count,
        SUM(revenue) as total_revenue
    FROM orders
    GROUP BY 1
    ORDER BY 1 DESC
    LIMIT 20
    """
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    
    # Check for the last few days specifically
    print("\n--- 🕵️ SPECIFIC GAP INVESTIGATION ---")
    dates_to_check = ['2026-02-13', '2026-02-14', '2026-02-15', '2026-02-16', '2026-02-17', '2026-02-18', '2026-02-19', '2026-02-20']
    for d in dates_to_check:
        count = pd.read_sql_query(f"SELECT COUNT(*) FROM orders WHERE DATE(order_time) = '{d}'", conn).iloc[0,0]
        print(f"Date: {d} | Orders: {count}")
    
    conn.close()

if __name__ == "__main__":
    audit_daily_counts()
