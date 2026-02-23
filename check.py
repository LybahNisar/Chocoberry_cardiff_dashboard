import sqlite3
conn = sqlite3.connect('restaurant_data.db')
c = conn.cursor()
c.execute("SELECT order_time, revenue FROM orders ORDER BY order_time DESC LIMIT 5")
for row in c.fetchall():
    print(row)
conn.close()