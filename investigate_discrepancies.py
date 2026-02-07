import pandas as pd

# Load data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")

# Check total rows
print("=" * 60)
print(f"Total rows in CSV: {len(sales_df)}")
print("Dashboard shows: 5,000 orders")
print(f"Difference: {len(sales_df) - 5000} order")
print("=" * 60)

# Check for any rows with null/empty values that might be filtered
print("\nChecking for rows with null 'Revenue':")
sales_df['Revenue'] = pd.to_numeric(sales_df['Revenue'], errors='coerce')
null_revenue = sales_df[sales_df['Revenue'].isna()]
print(f"Rows with null Revenue: {len(null_revenue)}")

if len(null_revenue) > 0:
    print("\nThese rows might be filtered out by the dashboard:")
    print(null_revenue[['Order ID', 'Gross sales', 'Revenue', 'Dispatch type']])

# Check Charges columns  
sales_df['Charges'] = pd.to_numeric(sales_df['Charges'], errors='coerce')
sales_df['Delivery charges'] =pd.to_numeric(sales_df['Delivery charges'], errors='coerce')

print("\n" + "=" * 60)
print("CHARGES COLUMNS:")
print("=" * 60)
print(f"'Charges' total: £{sales_df['Charges'].sum():,.2f}")
print(f"'Delivery charges' total: £{sales_df['Delivery charges'].sum():,.2f}")
print("\nDashboard shows: £140.36")
print("\n⚠️ NEITHER COLUMN MATCHES THE DASHBOARD!")
print("=" * 60)
