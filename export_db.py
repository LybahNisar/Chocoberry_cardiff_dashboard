import sqlite3
import pandas as pd
from pathlib import Path

# Path to your database
db_path = Path('C:/Users/GEO/Desktop/Dashboard/restaurant_data.db')
output_file = 'DATABASE_EXPORT.csv'

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
else:
    try:
        print("Reading database...")
        conn = sqlite3.connect(str(db_path))
        
        # Pull all orders
        df = pd.read_sql_query("SELECT * FROM orders ORDER BY order_time DESC", conn)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"✅ SUCCESS! Exported {len(df)} orders to '{output_file}'")
        print("You can now open DATABASE_EXPORT.csv in Excel to see all your data.")
        
        conn.close()
    except Exception as e:
        print(f"❌ Error during export: {e}")
