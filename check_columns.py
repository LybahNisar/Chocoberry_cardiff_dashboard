import pandas as pd
from pathlib import Path

# Load the data
data_path = Path(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff")
sales_df = pd.read_csv(data_path / "sales_data.csv")

# Convert columns
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'], errors='coerce')
sales_df['Revenue'] = pd.to_numeric(sales_df['Revenue'], errors='coerce')
sales_df['Tax on gross sales'] = pd.to_numeric(sales_df['Tax on gross sales'], errors='coerce')

output = []
output.append("COLUMN COMPARISON:")
output.append("=" * 60)
output.append(f"\nTotal using 'Gross sales': £{sales_df['Gross sales'].sum():,.2f}")
output.append(f"Total using 'Revenue': £{sales_df['Revenue'].sum():,.2f}")
output.append(f"\nTotal Orders: {len(sales_df):,}")
output.append(f"Average Order (Gross sales): £{sales_df['Gross sales'].mean():,.2f}")
output.append(f"Total Tax: £{sales_df['Tax on gross sales'].sum():,.2f}")

output.append("\n" + "=" * 60)
output.append("DASHBOARD USES 'Revenue' COLUMN")
output.append("=" * 60)

with open('column_check_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Saved to column_check_results.txt")
