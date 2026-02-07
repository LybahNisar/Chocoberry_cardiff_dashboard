import pandas as pd

# Load data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")

# Convert numeric columns
sales_df['Revenue'] = pd.to_numeric(sales_df['Revenue'], errors='coerce')
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'], errors='coerce')
sales_df['Tax on gross sales'] = pd.to_numeric(sales_df['Tax on gross sales'], errors='coerce')
sales_df['Delivery charges'] = pd.to_numeric(sales_df['Delivery charges'], errors='coerce')

# Calculate metrics
total_revenue = sales_df['Revenue'].sum()
total_orders = len(sales_df)
avg_order = sales_df['Gross sales'].mean()
total_tax = sales_df['Tax on gross sales'].sum()
delivery_charges = sales_df['Delivery charges'].sum()

output = []
output.append("CSV CALCULATIONS:")
output.append("=" * 60)
output.append(f"Total Revenue: £{total_revenue:,.2f} (£{total_revenue/1000:.1f}K)")
output.append(f"Average Order: £{avg_order:.2f}")
output.append(f"Total Orders: {total_orders:,}")
output.append(f"Total Tax: £{total_tax:,.2f} (£{total_tax/1000:.1f}K)")
output.append(f"Delivery Charges: £{delivery_charges:.2f}")
output.append("=" * 60)

output.append("\nYOUR DASHBOARD SHOWS:")
output.append("=" * 60)
output.append("Total Revenue: £76.9K")
output.append("Average Order: £14.77")
output.append("Total Orders: 5,000")
output.append("Total Tax: £2.9K")
output.append("Delivery Charges: £140.36")
output.append("=" * 60)

# Check matches
output.append("\nVERIFICATION:")
output.append("=" * 60)

rev_match = abs(total_revenue/1000 - 76.9) < 0.1
avg_match = abs(avg_order - 14.77) < 0.01
ord_match = total_orders == 5000
tax_match = abs(total_tax/1000 - 2.9) < 0.1
del_match = abs(delivery_charges - 140.36) < 0.01

output.append(f"Revenue: {'✅ MATCH' if rev_match else '❌ NO MATCH'}")
output.append(f"Avg Order: {'✅ MATCH' if avg_match else '❌ NO MATCH'}")
output.append(f"Orders: {'✅ MATCH' if ord_match else '❌ NO MATCH'}")
output.append(f"Tax: {'✅ MATCH' if tax_match else '❌ NO MATCH'}")
output.append(f"Delivery: {'✅ MATCH' if del_match else '❌ NO MATCH'}")
output.append("=" * 60)

# Overall
if all([rev_match, avg_match, ord_match, tax_match, del_match]):
    output.append("\n✅ DASHBOARD IS 100% ACCURATE!")
    output.append("All numbers match the CSV data perfectly.")
    output.append("SAFE TO SEND TO CLIENT!")
else:
    output.append("\n❌ DISCREPANCIES FOUND!")
    output.append("Do not send to client until resolved.")

with open('dashboard_verification_final.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Results saved to dashboard_verification_final.txt")
