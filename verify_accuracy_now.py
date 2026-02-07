import pandas as pd
from pathlib import Path

output = []
output.append("=" * 60)
output.append("DASHBOARD ACCURACY VERIFICATION")
output.append("=" * 60)

# Load the data
data_path = Path(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff")
sales_df = pd.read_csv(data_path / "sales_data.csv")

# Clean and convert
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'].astype(str).str.replace('£', '').str.replace(',', ''), errors='coerce')
sales_df['Revenue'] = pd.to_numeric(sales_df['Revenue'].astype(str).str.replace('£', '').str.replace(',', ''), errors='coerce')
sales_df['Tax on gross sales'] = pd.to_numeric(sales_df['Tax on gross sales'].astype(str).str.replace('£', '').str.replace(',', ''), errors='coerce')
sales_df['Delivery charges'] = pd.to_numeric(sales_df['Delivery charges'].astype(str).str.replace('£', '').str.replace(',', ''), errors='coerce')

# Calculate metrics
total_revenue = sales_df['Gross sales'].sum()
total_orders = len(sales_df)
avg_order = total_revenue / total_orders if total_orders > 0 else 0
total_tax = sales_df['Tax on gross sales'].sum()
delivery_charges = sales_df['Delivery charges'].sum()

output.append("\n📊 CALCULATED FROM CSV:")
output.append(f"Total Revenue: £{total_revenue:,.2f}")
output.append(f"Total Orders: {total_orders:,}")
output.append(f"Average Order: £{avg_order:,.2f}")
output.append(f"Total Tax: £{total_tax:,.2f}")
output.append(f"Delivery Charges: £{delivery_charges:,.2f}")

# Date range
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'])
start_date = sales_df['Order time'].min()
end_date = sales_df['Order time'].max()

output.append(f"\nDate Range: {start_date.date()} to {end_date.date()}")
output.append(f"Total Days: {(end_date - start_date).days + 1}")

# Peak hours
sales_df['hour'] = sales_df['Order time'].dt.hour
hourly_sales = sales_df.groupby('hour')['Gross sales'].sum().sort_values(ascending=False)
output.append(f"\n🕐 TOP 3 PEAK HOURS (by revenue):")
for i, (hour, revenue) in enumerate(hourly_sales.head(3).items(), 1):
    output.append(f"{i}. {hour}:00 - £{revenue:,.2f}")

# Dispatch types
dispatch_sales = sales_df.groupby('Dispatch type')['Gross sales'].sum().sort_values(ascending=False)
output.append(f"\n🚚 SALES BY DISPATCH TYPE:")
for dispatch, revenue in dispatch_sales.items():
    output.append(f"{dispatch}: £{revenue:,.2f}")

output.append("\n" + "=" * 60)
output.append("✅ Verification complete. Compare these with your dashboard.")
output.append("=" * 60)

# Write to file
with open('verification_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Results saved to verification_results.txt")
