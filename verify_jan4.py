import pandas as pd

# Load transaction data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'])
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'], errors='coerce').fillna(0)

# Filter Jan 4, 2026 only
jan4_orders = sales_df[sales_df['Order time'].dt.date == pd.to_datetime('2026-01-04').date()]

output = []
output.append("JAN 4, 2026 VERIFICATION")
output.append("=" * 70)
output.append(f"Total orders on Jan 4: {len(jan4_orders)}")
output.append(f"Total Gross Sales: £{jan4_orders['Gross sales'].sum():,.2f}")
output.append("=" * 70)

output.append("\nFIRST 10 ORDERS ON JAN 4:")
output.append("=" * 70)
for idx, row in jan4_orders.head(10).iterrows():
    output.append(f"{row['Order time']}: £{row['Gross sales']:.2f}")
output.append("=" * 70)

output.append("\nCOMPARISON:")
output.append("=" * 70)
output.append("Dashboard shows: £885.51")
output.append(f"Actual total from CSV: £{jan4_orders['Gross sales'].sum():,.2f}")
output.append(f"Pre-aggregated file shows: £3,690.21")
output.append("=" * 70)

with open('jan4_verification.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Saved to jan4_verification.txt")
