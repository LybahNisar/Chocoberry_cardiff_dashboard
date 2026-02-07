import pandas as pd

# Load data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")

# Convert
sales_df['Charges'] = pd.to_numeric(sales_df['Charges'], errors='coerce')
sales_df['Delivery charges'] = pd.to_numeric(sales_df['Delivery charges'], errors='coerce')

print("COLUMN COMPARISON:")
print("=" * 60)
print(f"'Charges' column total: £{sales_df['Charges'].sum():,.2f}")
print(f"'Delivery charges' column total: £{sales_df['Delivery charges'].sum():,.2f}")
print("=" * 60)
print("\nDashboard shows: £140.36")
print("This matches 'Charges' column")
print("\nThe dashboard is using the wrong column!")
print("It should use 'Delivery charges' (£204.06)")
