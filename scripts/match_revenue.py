import pandas as pd
import sqlite3

# Load CSV and clean revenue
csv = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
for col in ['Revenue']:
    if csv[col].dtype == 'object':
        csv[col] = csv[col].str.replace(',', '', regex=False)
    csv[col] = pd.to_numeric(csv[col], errors='coerce').fillna(0)

csv['Order ID'] = csv['Order ID'].astype(str)

# Load DB and clean revenue
conn = sqlite3.connect('restaurant_data.db')
db = pd.read_sql_query("SELECT order_id, revenue FROM orders", conn)
conn.close()
db['order_id'] = db['order_id'].astype(str)

# Merge
merged = csv[['Order ID', 'Revenue']].merge(
    db[['order_id', 'revenue']], 
    left_on='Order ID', right_on='order_id', how='inner'
)

# Find differences
merged['diff'] = merged['Revenue'] - merged['revenue']
mismatches = merged[abs(merged['diff']) > 0.01]

print(f"Total matched orders: {len(merged)}")
print(f"Number of mismatches: {len(mismatches)}")
print(f"Total revenue difference on matched: {mismatches['diff'].sum():.2f}")

if len(mismatches) > 0:
    print("\nSample mismatches:")
    for _, r in mismatches.head(10).iterrows():
        print(f"ID: {r['Order ID']}, CSV: {r['Revenue']:.2f}, DB: {r['revenue']:.2f}, Diff: {r['diff']:.2f}")
