import sqlite3

conn = sqlite3.connect('restaurant_data.db')
c = conn.cursor()

# Fix existing Pickup -> Collection
c.execute("UPDATE orders SET dispatch_type = 'Collection' WHERE dispatch_type = 'Pickup'")
print('Fixed Pickup->Collection:', c.rowcount, 'rows')

# Fix DineIn -> Dine In  
c.execute("UPDATE orders SET dispatch_type = 'Dine In' WHERE dispatch_type = 'DineIn'")
print('Fixed DineIn->Dine In:', c.rowcount, 'rows')

conn.commit()

# Verify dispatch types now
c.execute('SELECT dispatch_type, COUNT(*) FROM orders GROUP BY dispatch_type ORDER BY COUNT(*) DESC')
print('\nDispatch types after fix:')
for r in c.fetchall():
    print(f'  {r[0]}: {r[1]}')

# Verify final stats
c.execute('SELECT COUNT(*) FROM orders')
print('\nTotal orders:', c.fetchone()[0])

c.execute("SELECT MIN(order_time), MAX(order_time) FROM orders WHERE order_time IS NOT NULL AND order_time != 'NaT'")
dates = c.fetchone()
print('Date range:', dates[0], 'to', dates[1])

conn.close()
