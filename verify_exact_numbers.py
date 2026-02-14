import pandas as pd
from pathlib import Path

# Load data
data_path = Path('data/raw/chocoberry_cardiff')
df = pd.read_csv(data_path / 'sales_data.csv')

# Show total rows first
print(f"Total rows in CSV: {len(df)}")

# Convert columns
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Revenue after refunds'] = pd.to_numeric(df['Revenue after refunds'], errors='coerce').fillna(0)
df['Order time'] = pd.to_datetime(df['Order time'])

# Filter EXACTLY like the dashboard
filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]

print(f"\nFiltered rows (Jan 4 - Feb 6, 2026): {len(filtered)}")

# Dashboard shows:
# - Total Revenue: £81.0K
# - Total Orders: 5,275
# - Average Order Value: £14.75

print("\n" + "="*60)
print("DASHBOARD SAYS:")
print("="*60)
print("Total Revenue: £81.0K")
print("Total Orders: 5,275")
print("Average Order Value: £14.75")

print("\n" + "="*60)
print("CSV DATA SAYS:")
print("="*60)
print(f"Total Orders: {len(filtered):,}")
print(f"Total Gross Sales: £{filtered['Gross sales'].sum():,.2f}")
print(f"Total Revenue: £{filtered['Revenue'].sum():,.2f}")
print(f"Total Revenue (after refunds): £{filtered['Revenue after refunds'].sum():,.2f}")

# Calculate AOV different ways
gross_aov = filtered['Gross sales'].sum() / len(filtered)
revenue_aov = filtered['Revenue'].sum() / len(filtered)
revenue_after_refunds_aov = filtered['Revenue after refunds'].sum() / len(filtered)

print(f"\nAverage Order Value (Gross Sales / Orders): £{gross_aov:.2f}")
print(f"Average Order Value (Revenue / Orders): £{revenue_aov:.2f}")
print(f"Average Order Value (Revenue after refunds / Orders): £{revenue_after_refunds_aov:.2f}")

print("\n" + "="*60)
print("VERDICT:")
print("="*60)

# Check if matches
if len(filtered) == 5275:
    print("✅ Order count MATCHES (5,275)")
else:
    print(f"❌ Order count MISMATCH: CSV has {len(filtered)}, Dashboard shows 5,275")

total_revenue_k = round(filtered['Revenue'].sum() / 1000, 1)
if total_revenue_k == 81.0:
    print(f"✅ Total Revenue MATCHES (£{total_revenue_k}K)")
else:
    print(f"❌ Total Revenue MISMATCH: CSV has £{total_revenue_k}K, Dashboard shows £81.0K")

if abs(gross_aov - 14.75) < 0.01:
    print(f"✅ Average Order Value MATCHES (£{gross_aov:.2f})")
else:
    print(f"❌ Average Order Value MISMATCH: CSV has £{gross_aov:.2f}, Dashboard shows £14.75")
