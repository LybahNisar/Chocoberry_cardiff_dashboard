import pandas as pd
from datetime import datetime

# REPLICATE EXACT DASHBOARD LOGIC
print("=" * 80)
print("FINAL VERIFICATION - Exact Dashboard Logic")
print("=" * 80)

# Load sales_data.csv (exactly as dashboard does)
sales_data = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
sales_data['Order time'] = pd.to_datetime(sales_data['Order time'])

# Convert numeric columns (exactly as dashboard does)
numeric_columns = ['Gross sales', 'Tax on gross sales', 'Tips', 'Delivery charges', 
                  'Service charges', 'DRS charges', 'Packaging charges', 
                  'Additional charges', 'Charges', 'Revenue', 'Refunds', 
                  'Revenue after refunds', 'Discounts']

for col in numeric_columns:
    if col in sales_data.columns:
        sales_data[col] = pd.to_numeric(sales_data[col], errors='coerce').fillna(0)

# Dashboard date filter (from screenshot: Jan 04 - Feb 06)
start_date = datetime(2026, 1, 4)
end_date = datetime(2026, 2, 6)

# Filter data (exactly as dashboard does)
filtered_sales = sales_data[
    (sales_data['Order time'] >= start_date) & 
    (sales_data['Order time'] <= end_date.replace(hour=23, minute=59, second=59))
]

# Calculate metrics (EXACTLY as dashboard does - lines 186-226)
total_revenue = filtered_sales['Revenue'].sum()
avg_order_value = filtered_sales['Gross sales'].mean()
total_orders = len(filtered_sales)
total_tax = filtered_sales['Tax on gross sales'].sum()
total_charges = filtered_sales['Charges'].sum()

# Format exactly as dashboard does
revenue_display = f"£{total_revenue/1000 :.1f}K" if total_revenue >= 1000 else f"£{total_revenue:,.2f}"
tax_display = f"£{total_tax/1000:.1f}K" if total_tax >= 1000 else f"£{total_tax:,.2f}"

print("\n📊 CALCULATED FROM SALES_DATA.CSV:")
print("-" * 80)
print(f"Total Revenue:        {revenue_display}")
print(f"  (actual value: £{total_revenue:,.2f})")
print(f"\nAverage Order:        £{avg_order_value:.2f}")
print(f"\nTotal Orders:         {total_orders:,}")
print(f"\nTotal Tax:            {tax_display}")
print(f"  (actual value: £{total_tax:,.2f})")
print(f"\nDelivery Charges:     £{total_charges:.2f}")

print("\n" + "=" * 80)
print("DASHBOARD DISPLAY (from screenshot):")
print("=" * 80)
print("Total Revenue:        £81.0K")
print("Average Order:        £14.75")
print("Total Orders:         5,275")
print("Total Tax:            £3.0K")
print("Delivery Charges:     £159.84")

print("\n" + "=" * 80)
print("COMPARISON:")
print("=" * 80)

revenue_match = abs(total_revenue - 81000) < 1000
avg_match = abs(avg_order_value - 14.75) < 0.01
orders_match = total_orders == 5275
tax_match = abs(total_tax - 3000) < 100
charges_match = abs(total_charges - 159.84) < 0.01

print(f"Revenue:    {'✅ MATCH' if revenue_match else '❌ MISMATCH'} (diff: £{abs(total_revenue - 81000):.2f})")
print(f"Avg Order:  {'✅ MATCH' if avg_match else '❌ MISMATCH'} (diff: £{abs(avg_order_value - 14.75):.2f})")
print(f"Orders:     {'✅ MATCH' if orders_match else '❌ MISMATCH'} (diff: {abs(total_orders - 5275)})")
print(f"Tax:        {'✅ MATCH' if tax_match else '❌ MISMATCH'} (diff: £{abs(total_tax - 3000):.2f})")
print(f"Charges:    {'✅ MATCH' if charges_match else '❌ MISMATCH'} (diff: £{abs(total_charges - 159.84):.2f})")

tests_passed = sum([revenue_match, avg_match, orders_match, tax_match, charges_match])

print("\n" + "=" * 80)
if tests_passed == 5:
    print("✅✅✅ ALL METRICS VERIFIED - NO HALLUCINATION ✅✅✅")
else:
    print(f"⚠️  {5 - tests_passed} METRIC(S) DO NOT MATCH")
print("=" * 80)

# Additional debug info
print(f"\nDebug Info:")
print(f"Total rows in sales_data.csv: {len(sales_data):,}")
print(f"Rows after date filter: {len(filtered_sales):,}")
print(f"Date range in filtered: {filtered_sales['Order time'].min().date()} to {filtered_sales['Order time'].max().date()}")
