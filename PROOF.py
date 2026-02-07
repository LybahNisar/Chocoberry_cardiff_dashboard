import pandas as pd

# Load your CSV
df = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06 23:59:59')]

# Convert to numeric
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)
df['Tax on gross sales'] = pd.to_numeric(df['Tax on gross sales'], errors='coerce').fillna(0)
df['Charges'] = pd.to_numeric(df['Charges'], errors='coerce').fillna(0)

# Calculate the 5 main metrics
total_revenue = df['Revenue'].sum()
total_orders = len(df)
avg_order = df['Gross sales'].mean()
total_tax = df['Tax on gross sales'].sum()
total_charges = df['Charges'].sum()

# Print clearly
print("DASHBOARD VERIFICATION - Jan 4 to Feb 6, 2026")
print("")
print("1. Total Revenue:")
print(f"   Calculated: £{total_revenue:,.2f}")
print(f"   Display:    £{total_revenue/1000:.1f}K")
print(f"   Expected:   £81.0K")
print(f"   Match:      {abs(total_revenue/1000 - 81.0) < 1}")
print("")
print("2. Total Orders:")
print(f"   Calculated: {total_orders:,}")
print(f"   Expected:   5,275")
print(f"   Match:      {total_orders == 5275}")
print("")
print("3. Average Order:")
print(f"   Calculated: £{avg_order:.2f}")
print(f"   Expected:   £14.75")
print(f"   Match:      {abs(avg_order - 14.75) < 0.01}")
print("")
print("4. Total Tax:")
print(f"   Calculated: £{total_tax:,.2f}")
print(f"   Display:    £{total_tax/1000:.1f}K")
print(f"   Expected:   £3.0K")
print(f"   Match:      {abs(total_tax/1000 - 3.0) < 0.1}")
print("")
print("5. Delivery Charges:")
print(f"   Calculated: £{total_charges:.2f}")
print(f"   Expected:   £159.84")
print(f"   Match:      {abs(total_charges - 159.84) < 0.01}")
print("")

# Overall
all_match = (
    abs(total_revenue/1000 - 81.0) < 1 and
    total_orders == 5275 and
    abs(avg_order - 14.75) < 0.01 and
    abs(total_tax/1000 - 3.0) < 0.1 and
    abs(total_charges - 159.84) < 0.01
)

if all_match:
    print("RESULT: ALL 5 METRICS MATCH - 100% ACCURATE")
else:
    print("RESULT: MISMATCH FOUND")
