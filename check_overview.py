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
print("=" * 80)
print("SALES_OVERVIEW.CSV - Date Range: Jan 4 - Feb 6, 2026")
print("=" * 80)

total_revenue = filtered['Gross sales'].sum()
total_tax = filtered['Tax on gross sales'].sum()
total_orders = filtered['Orders'].sum()
total_charges = filtered['Charges'].sum()

print(f"\nTotal Revenue (Gross sales):  £{total_revenue:,.2f}")
print(f"Total Tax:                     £{total_tax:,.2f}")  
print(f"Total Orders:                  {int(total_orders):,}")
print(f"Total Charges:                 £{total_charges:,.2f}")

print(f"\nAverage Order:                 £{total_revenue/total_orders:.2f}")

print("\n" + "=" * 80)
print("COMPARISON TO DASHBOARD")
print("=" * 80)

print(f"\nDashboard shows:   £81.0K revenue, 5,275 orders")
print(f"sales_overview:    £{total_revenue/1000:.1f}K revenue, {int(total_orders):,} orders")

print(f"\nMatch: {'✅ YES' if abs(total_revenue - 81000) < 1000 else '❌ NO'}")

# Show the days
print("\n" + "=" * 80)
print("DAILY BREAKDOWN")
print("=" * 80)
print(filtered[['Order time', 'Gross sales', 'Orders']].to_string(index=False))
