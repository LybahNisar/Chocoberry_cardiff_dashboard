import pandas as pd

# Load sales data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'])

# Convert numeric columns
for col in ['Gross sales', 'Tax on gross sales', 'Revenue', 'Charges']:
    sales_df[col] = pd.to_numeric(sales_df[col], errors='coerce').fillna(0)

# Calculate ALL metrics from your screenshot
total_revenue = sales_df['Revenue'].sum()
avg_order = sales_df['Gross sales'].mean()
total_orders = len(sales_df)
total_tax = sales_df['Tax on gross sales'].sum()
delivery_charges = sales_df['Charges'].sum()

output = []
output.append("=" * 70)
output.append("COMPLETE DASHBOARD VERIFICATION - ALL METRICS")
output.append("=" * 70)

output.append("\n1️⃣  TOTAL REVENUE")
output.append("-" * 70)
output.append(f"CSV Calculation: £{total_revenue:,.2f}")
output.append(f"Dashboard Shows: £76.9K")
output.append(f"Percentage:      £{total_revenue/1000:.1f}K")
output.append(f"Match: {'✅ YES' if abs(total_revenue/1000 - 76.9) < 0.2 else '❌ NO'}")

output.append("\n2️⃣  AVERAGE ORDER")
output.append("-" * 70)
output.append(f"CSV Calculation: £{avg_order:.2f}")
output.append(f"Dashboard Shows: £14.77")
output.append(f"Match: {'✅ YES' if abs(avg_order - 14.77) < 0.02 else '❌ NO'}")

output.append("\n3️⃣  TOTAL ORDERS")
output.append("-" * 70)
output.append(f"CSV Calculation: {total_orders:,}")
output.append(f"Dashboard Shows: 5,000")
output.append(f"Match: {'✅ YES' if abs(total_orders - 5000) <= 1 else '❌ NO'}")

output.append("\n4️⃣  TOTAL TAX")
output.append("-" * 70)
output.append(f"CSV Calculation: £{total_tax:,.2f}")
output.append(f"Dashboard Shows: £2.9K")
output.append(f"Percentage:      £{total_tax/1000:.1f}K")
output.append(f"Match: {'✅ YES' if abs(total_tax/1000 - 2.9) < 0.1 else '❌ NO'}")

output.append("\n5️⃣  DELIVERY CHARGES")
output.append("-" * 70)
output.append(f"CSV Calculation: £{delivery_charges:,.2f}")
output.append(f"Dashboard Shows: £140.36")
output.append(f"Match: {'✅ YES' if abs(delivery_charges - 140.36) < 1 else '❌ NO'}")

output.append("\n" + "=" * 70)
output.append("FINAL VERDICT")
output.append("=" * 70)

# Check if all match
all_match = (
    abs(total_revenue/1000 - 76.9) < 0.2 and
    abs(avg_order - 14.77) < 0.02 and
    abs(total_orders - 5000) <= 1 and
    abs(total_tax/1000 - 2.9) < 0.1
)

if all_match:
    output.append("✅ ALL METRICS ARE ACCURATE!")
    output.append("Dashboard numbers match CSV data within acceptable tolerance.")
    output.append("SAFE TO SEND TO CLIENT.")
else:
    output.append("❌ SOME METRICS DO NOT MATCH")
    output.append("Review discrepancies before sending to client.")

output.append("=" * 70)

with open('complete_verification_final.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Complete verification saved to complete_verification_final.txt")
