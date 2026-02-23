import sqlite3
import pandas as pd

conn = sqlite3.connect('restaurant_data.db')
query = "SELECT date(order_time) as Date, count(*) as Orders, sum(revenue) as Revenue FROM orders GROUP BY Date ORDER BY Date DESC LIMIT 10"
df = pd.read_sql_query(query, conn)
print(df)
conn.close()
