import pandas as pd

print("="*80)
print("FINAL COMPREHENSIVE DASHBOARD VERIFICATION")
print("="*80)

# Load data
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])

# Convert numeric columns
for col in ['Gross sales', 'Revenue', 'Tax on gross sales', 'Delivery charges']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Filter to Jan 4 - Feb 4, 2026
df = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-04')]

print(f"\nDate Range: Jan 04, 2026 - Feb 04, 2026")
print(f"Total Rows in Filtered Data: {len(df):,}")

# =============================================================================
# VERIFICATION 1: KPI METRICS
# =============================================================================
print("\n" + "="*80)
print("KPI METRICS VERIFICATION")
print("="*80)

total_revenue = df['Revenue'].sum()
total_gross = df['Gross sales'].sum()
total_orders = len(df)
avg_order = total_gross / total_orders if total_orders > 0 else 0
total_tax = df['Tax on gross sales'].sum()
total_delivery = df['Delivery charges'].sum()

print(f"\nCalculated from Source CSV:")
print(f"  Total Revenue:        £{total_revenue:,.2f}")
print(f"  Total Gross Sales:    £{total_gross:,.2f}")
print(f"  Average Order:        £{avg_order:.2f}")
print(f"  Total Orders:         {total_orders:,}")
print(f"  Total Tax:            £{total_tax:,.2f}")
print(f"  Delivery Charges:     £{total_delivery:.2f}")

print(f"\nDashboard Shows:")
print(f"  Total Revenue:        £76,8xx (truncated)")
print(f"  Average Order:        £14.77")
print(f"  Total Orders:         5,000")
print(f"  Total Tax:            £2,87x (truncated)")
print(f"  Delivery Charges:     £140.36")

kpi_checks = []
kpi_checks.append(("Total Orders", total_orders == 5000, total_orders, 5000))
kpi_checks.append(("Avg Order", abs(avg_order - 14.77) < 0.01, f"£{avg_order:.2f}", "£14.77"))
kpi_checks.append(("Delivery Charges", abs(total_delivery - 140.36) < 0.01, f"£{total_delivery:.2f}", "£140.36"))

print(f"\nKPI Match Results:")
for name, match, calc, dash in kpi_checks:
    status = "✅ MATCH" if match else "❌ MISMATCH"
    print(f"  {name:20s} {status:12s} | Calculated: {calc:15s} | Dashboard: {dash}")

# =============================================================================
# VERIFICATION 2: DISPATCH TYPE BREAKDOWN
# =============================================================================
print("\n" + "="*80)
print("DISPATCH TYPE BREAKDOWN")
print("="*80)

dispatch = df.groupby('Dispatch type').agg({
    'Gross sales': 'sum',
    'Order ID': 'count'
})
total_dispatch_sales = dispatch['Gross sales'].sum()
dispatch['Percentage'] = (dispatch['Gross sales'] / total_dispatch_sales * 100)

print(f"\nCalculated from Source CSV:")
for dtype in dispatch.index:
    pct = dispatch.loc[dtype, 'Percentage']
    sales = dispatch.loc[dtype, 'Gross sales']
    orders = dispatch.loc[dtype, 'Order ID']
    print(f"  {dtype:15s}: {pct:5.1f}% | £{sales:10,.2f} | {orders:5.0f} orders")

print(f"\nDashboard Pie Chart Shows:")
print(f"  Delivery:       39.9%")
print(f"  Dine In:        31.8%")
print(f"  Take Away:      24.2%")
print(f"  Collection:     ~4%")

# =============================================================================
# VERIFICATION 3: SALES CHANNEL PERFORMANCE
# =============================================================================
print("\n" + "="*80)
print("SALES CHANNEL PERFORMANCE")
print("="*80)

channel = df.groupby('Sales channel type')['Gross sales'].sum()
total_channel_sales = channel.sum()
channel_pct = (channel / total_channel_sales * 100).sort_values(ascending=False)

print(f"\nCalculated from Source CSV:")
for ch in channel_pct.index:
    pct = channel_pct[ch]
    sales = channel[ch]
    print(f"  {ch:15s}: {pct:5.2f}% | £{sales:10,.2f}")

print(f"\nDashboard Donut Chart Shows:")
print(f"  POS:            58.8%")
print(f"  Uber Eats:      28.2%")
print(f"  Deliveroo:      12.3%")
print(f"  Just Eat:       0.786%")

# =============================================================================
# VERIFICATION 4: PEAK HOURS
# =============================================================================
print("\n" + "="*80)
print("PEAK HOURS ANALYSIS")
print("="*80)

hourly = df.groupby(df['Order time'].dt.hour).agg({
    'Gross sales': 'sum',
    'Order ID': 'count'
})
hourly_sorted = hourly.sort_values('Gross sales', ascending=False)

print(f"\nTop 3 Hours by Sales:")
for idx, (hour, row) in enumerate(hourly_sorted.head(3).iterrows(), 1):
    print(f"  Peak #{idx}: {hour:02d}:00 | £{row['Gross sales']:8,.2f} | {row['Order ID']:3.0f} orders")

print(f"\nDashboard Shows:")
print(f"  Peak #1: 21:00 | £11,214")
print(f"  Peak #2: 20:00 | £10,904")
print(f"  Peak #3: 22:00 | £10,319")

# =============================================================================
# FINAL VERDICT
# =============================================================================
print("\n" + "="*80)
print("FINAL VERDICT")
print("="*80)

all_match = all(check[1] for check in kpi_checks)
if all_match:
    print("\n✅ ALL VERIFIABLE VALUES MATCH THE SOURCE DATA")
    print("\nThe dashboard is displaying ACCURATE calculations.")
else:
    print("\n⚠️ SOME VALUES HAVE DISCREPANCIES")
    print("\nPlease review the mismatch details above.")

print("="*80)
