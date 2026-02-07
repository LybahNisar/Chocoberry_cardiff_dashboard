import pandas as pd

# Load and prep data exactly like dashboard does
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'])

# Convert numeric columns
for col in ['Gross sales', 'Tax on gross sales', 'Tips', 'Delivery charges', 
            'Service charges', 'DRS charges', 'Packaging charges', 
            'Additional charges', 'Charges', 'Revenue', 'Refunds', 
            'Revenue after refunds', 'Discounts']:
    if col in sales_df.columns:
        sales_df[col] = pd.to_numeric(sales_df[col], errors='coerce').fillna(0)

# Filter to Jan 4 - Feb 4, 2026 (date range from screenshot)
filtered = sales_df[(sales_df['Order time'] >= '2026-01-04') & 
                    (sales_df['Order time'] <= '2026-02-04')]

output = []
output.append("FILTERED DATA (Jan 4 - Feb 4, 2026):")
output.append("=" * 60)
output.append(f"Total Orders: {len(filtered):,}")
output.append(f"Total Revenue: £{filtered['Revenue'].sum():,.2f} (£{filtered['Revenue'].sum()/1000:.1f}K)")
output.append(f"Average Order: £{filtered['Gross sales'].mean():,.2f}")
output.append(f"Total Tax: £{filtered['Tax on gross sales'].sum():,.2f} (£{filtered['Tax on gross sales'].sum()/1000:.1f}K)")
output.append(f"'Charges' column: £{filtered['Charges'].sum():,.2f}")
output.append(f"'Delivery charges' column: £{filtered['Delivery charges'].sum():,.2f}")
output.append("=" * 60)

with open('filtered_comparison.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
    
print("Saved to filtered_comparison.txt")
