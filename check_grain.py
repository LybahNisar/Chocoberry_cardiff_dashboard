import pandas as pd
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
num_rows = len(df)
num_orders = df['Order ID'].nunique()
print(f"Total Rows: {num_rows}")
print(f"Unique Orders: {num_orders}")
if num_rows == num_orders:
    print("Each row is one order (Summary Data)")
else:
    print("Multiple rows per order (Item Data)")
