import sqlite3
import pandas as pd

conn = sqlite3.connect('restaurant_data.db')
# Max date in CSV was 2026-02-13 00:49:00
df = pd.read_sql_query("SELECT order_id, order_time, revenue, dispatch_type, payment_method FROM orders WHERE order_time > '2026-02-13' ORDER BY order_time", conn)
conn.close()

print(f"Total API orders found: {len(df)}")
print(f"Total API revenue: {df['revenue'].sum():.2f}")
print("\nAPI Orders Detail:")
for _, r in df.iterrows():
    print(f"Time: {r['order_time']}, ID: {r['order_id']}, Rev: {r['revenue']:.2f}, Type: {r['dispatch_type']}, Pay: {r['payment_method']}")
