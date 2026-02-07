import pandas as pd

# Load sales_overview.csv
df = pd.read_csv("C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_overview.csv")

# Convert date
df['Order time'] = pd.to_datetime(df['Order time'], errors='coerce')

# Filter for Jan 4 - Feb 6, 2026
filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]

# Convert Gross sales to numeric (remove commas)
for col in ['Gross sales', 'Tax on gross sales', 'Charges', 'Revenue', 'Orders']:
    if col in filtered.columns:
        filtered[col] = pd.to_numeric(filtered[col].astype(str).str.replace(',', ''), errors='coerce')

# Calculate totals
total_revenue = filtered['Gross sales'].sum()
total_tax = filtered['Tax on gross sales'].sum()
total_orders = filtered['Orders'].sum()
total_charges = filtered['Charges'].sum()

print("sales_overview.csv | Jan 4 - Feb 6, 2026")
print(f"Revenue: {total_revenue:.2f} ({total_revenue/1000:.1f}K)")
print(f"Orders: {int(total_orders)}")
print(f"Tax: {total_tax:.2f}")
print(f"Charges: {total_charges:.2f}")
print(f"Avg Order: {total_revenue/total_orders:.2f}")
