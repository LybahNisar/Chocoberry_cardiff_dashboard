import pandas as pd
from datetime import datetime

# Load and process exactly as dashboard does
sales_data = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
sales_data['Order time'] = pd.to_datetime(sales_data['Order time'])

numeric_columns = ['Gross sales', 'Tax on gross sales', 'Tips', 'Delivery charges', 
                  'Service charges', 'DRS charges', 'Packaging charges', 
                  'Additional charges', 'Charges', 'Revenue', 'Refunds', 
                  'Revenue after refunds', 'Discounts']

for col in numeric_columns:
    if col in sales_data.columns:
        sales_data[col] = pd.to_numeric(sales_data[col], errors='coerce').fillna(0)

# Filter: Jan 4 - Feb 6, 2026
filtered_sales = sales_data[
    (sales_data['Order time'] >= datetime(2026, 1, 4)) & 
    (sales_data['Order time'] <= datetime(2026, 2, 6, 23, 59, 59))
]

# Calculate EXACTLY as dashboard (lines 186-226)
total_revenue = filtered_sales['Revenue'].sum()
avg_order = filtered_sales['Gross sales'].mean()
total_orders = len(filtered_sales)
total_tax = filtered_sales['Tax on gross sales'].sum()
total_charges = filtered_sales['Charges'].sum()

# Check matches
revenue_ok = abs(total_revenue/1000 - 81.0) < 1.0  # Within 1K
avg_ok = abs(avg_order - 14.75) < 0.01
orders_ok = total_orders == 5275
tax_ok = abs(total_tax/1000 - 3.0) < 0.1  # Within 100
charges_ok = abs(total_charges - 159.84) < 0.01

# Results
print("DASHBOARD vs CSV:")
print(f"Revenue:  {total_revenue/1000:.1f}K vs 81.0K - {'MATCH' if revenue_ok else 'DIFF'}")
print(f"Avg:      {avg_order:.2f} vs 14.75 - {'MATCH' if avg_ok else 'DIFF'}")
print(f"Orders:   {total_orders} vs 5,275 - {'MATCH' if orders_ok else 'DIFF'}")
print(f"Tax:      {total_tax/1000:.1f}K vs 3.0K - {'MATCH' if tax_ok else 'DIFF'}")
print(f"Charges:  {total_charges:.2f} vs 159.84 - {'MATCH' if charges_ok else 'DIFF'}")
all_ok = revenue_ok and avg_ok and orders_ok and tax_ok and charges_ok
print(f"\nRESULT: {'ALL CORRECT' if all_ok else 'ERRORS FOUND'}")
