import pandas as pd
import sqlite3

csv = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
for col in ['Revenue']:
    if csv[col].dtype == 'object':
        csv[col] = csv[col].str.replace(',', '', regex=False)
    csv[col] = pd.to_numeric(csv[col], errors='coerce').fillna(0)

conn = sqlite3.connect('restaurant_data.db')
db = pd.read_sql_query('SELECT order_id, revenue FROM orders', conn)
conn.close()

csv['Order ID'] = csv['Order ID'].astype(str)
db['order_id'] = db['order_id'].astype(str)

csv_ids = set(csv['Order ID'])
db_ids = set(db['order_id'])
missing = csv_ids - db_ids

print('MISSING_COUNT=' + str(len(missing)))
missing_rows = csv[csv['Order ID'].isin(missing)]
print('MISSING_REVENUE=' + str(round(missing_rows['Revenue'].sum(), 2)))

# Show the missing order IDs
for oid in sorted(missing)[:10]:
    row = csv[csv['Order ID'] == oid].iloc[0]
    print('MISSING_ID=' + oid + ' REV=' + str(row['Revenue']))

# Check revenue mismatch for MATCHED orders
merged = csv[['Order ID', 'Revenue']].merge(
    db[['order_id', 'revenue']], 
    left_on='Order ID', right_on='order_id', how='inner'
)
merged['diff'] = abs(merged['Revenue'] - merged['revenue'])
big_diff = merged[merged['diff'] > 0.01]
print('MISMATCHED_ORDERS=' + str(len(big_diff)))
print('MISMATCH_TOTAL=' + str(round(big_diff['diff'].sum(), 2)))

# Show worst mismatches
for _, r in big_diff.nlargest(5, 'diff').iterrows():
    print('MISMATCH: ID=' + str(r['Order ID']) + ' CSV=' + str(r['Revenue']) + ' DB=' + str(r['revenue']))
