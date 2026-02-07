import pandas as pd

# Load sales data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")

# Convert numeric columns
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'], errors='coerce').fillna(0)
sales_df['Revenue'] = pd.to_numeric(sales_df['Revenue'], errors='coerce').fillna(0)

# Group by Dispatch Type
dispatch_revenue = sales_df.groupby('Dispatch type')['Gross sales'].sum()
dispatch_orders = sales_df.groupby('Dispatch type').size()

# Calculate percentages
total_revenue = dispatch_revenue.sum()
revenue_pct = (dispatch_revenue / total_revenue * 100).round(1)

# Sort by revenue (descending)
dispatch_revenue = dispatch_revenue.sort_values(ascending=False)
revenue_pct = revenue_pct[dispatch_revenue.index]
dispatch_orders = dispatch_orders[dispatch_revenue.index]

output = []
output.append("DISPATCH TYPE VERIFICATION")
output.append("=" * 70)
output.append("\nREVENUE BY DISPATCH TYPE:")
output.append("-" * 70)
for dispatch_type in dispatch_revenue.index:
    output.append(f"{dispatch_type:15} £{dispatch_revenue[dispatch_type]:>10,.2f}  ({revenue_pct[dispatch_type]:>5.1f}%)")

output.append("\nORDER COUNT BY DISPATCH TYPE:")
output.append("-" * 70)
for dispatch_type in dispatch_orders.index:
    output.append(f"{dispatch_type:15} {dispatch_orders[dispatch_type]:>10,} orders")

output.append("\n" + "=" * 70)
output.append("DASHBOARD SHOWS (from your screenshot):")
output.append("-" * 70)
output.append("Revenue Distribution:")
output.append("  Delivery:    39.9%")
output.append("  Dine In:     31.8%")
output.append("  Take Away:   24.2%")
output.append("  Collection:   4.1%")
output.append("\nOrder Counts (approx from bar chart):")
output.append("  Delivery:   ~1650 orders")
output.append("  Dine In:    ~1850 orders")
output.append("  Take Away:  ~1500 orders")
output.append("  Collection:  ~200 orders")
output.append("=" * 70)

with open('dispatch_verification.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Saved to dispatch_verification.txt")
