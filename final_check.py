import pandas as pd

# Load data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")

# Convert numeric
sales_df['Revenue'] = pd.to_numeric(sales_df['Revenue'], errors='coerce')
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'], errors='coerce')
sales_df['Tax on gross sales'] = pd.to_numeric(sales_df['Tax on gross sales'], errors='coerce')

# Calculate what dashboard should show
print("WHAT YOUR DASHBOARD SHOULD SHOW:")
print("=" * 50)
print(f"Total Revenue: £{sales_df['Revenue'].sum():,.2f}")
print(f"Average Order: £{sales_df['Gross sales'].mean():,.2f}")
print(f"Total Orders: {len(sales_df):,}")
print(f"Total Tax: £{sales_df['Tax on gross sales'].sum():,.2f}")
print("=" * 50)
print("\nThese numbers should MATCH what you see in the dashboard.")
print("Open your local dashboard and verify!")
