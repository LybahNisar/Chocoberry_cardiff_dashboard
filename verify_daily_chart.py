import pandas as pd

# Load main sales data (same as dashboard)
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'])

# Convert numeric columns (same as dashboard)
for col in ['Gross sales', 'Revenue']:
    sales_df[col] = pd.to_numeric(sales_df[col], errors='coerce').fillna(0)

# Filter to date range from screenshot (Jan 4 - Feb 4, 2026)
filtered = sales_df[(sales_df['Order time'] >= '2026-01-04') & 
                    (sales_df['Order time'] <= '2026-02-04')]

# Group by date (EXACTLY like dashboard code does)
daily_sales = filtered.groupby(filtered['Order time'].dt.date).agg({
    'Gross sales': 'sum',
    'Revenue': 'sum',
    'Order ID': 'count'
}).reset_index()
daily_sales.columns = ['Date', 'Gross Sales', 'Revenue', 'Orders']

output = []
output.append("DAILY SALES DATA (from filtered transactions):")
output.append("=" * 70)
output.append(daily_sales.to_string(index=False))
output.append("=" * 70)

# Check key dates from chart
output.append("\nKEY DATES TO VERIFY AGAINST CHART:")
output.append("=" * 70)
jan_4 = daily_sales[daily_sales['Date'] == pd.to_datetime('2026-01-04').date()]
jan_31 = daily_sales[daily_sales['Date'] == pd.to_datetime('2026-01-31').date()]
feb_4 = daily_sales[daily_sales['Date'] == pd.to_datetime('2026-02-04').date()]

if len(jan_4) > 0:
    output.append(f"Jan 4: Gross Sales = £{jan_4['Gross Sales'].values[0]:,.2f}")
if len(jan_31) > 0:
    output.append(f"Jan 31 (peak): Gross Sales = £{jan_31['Gross Sales'].values[0]:,.2f}")
if len(feb_4) > 0:
    output.append(f"Feb 4 (end): Gross Sales = £{feb_4['Gross Sales'].values[0]:,.2f}")
output.append("=" * 70)

output.append("\nCheck these numbers against your chart!")
output.append("Jan 31 should show peak around 3800-4000")
output.append("Feb 4 should drop to very low (around 200)")

# Now load pre-aggregated file to compare
daily_csv = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\gross_sales_per_day.csv")
daily_csv['Order time'] = pd.to_datetime(daily_csv['Order time'])
daily_csv = daily_csv[(daily_csv['Order time'] >= '2026-01-04') & (daily_csv['Order time'] <= '2026-02-04')]

output.append("\nCOMPARISON WITH PRE-AGGREGATED CSV:")
output.append("=" * 70)
jan4_csv = daily_csv[daily_csv['Order time'] == '2026-01-04']
if len(jan4_csv) > 0:
    output.append(f"Pre-aggregated CSV shows Jan 4: £{jan4_csv['Gross sales'].values[0]}")
    output.append(f"Dashboard calculates Jan 4: £{jan_4['Gross Sales'].values[0]:,.2f if len(jan_4) > 0 else 0}")
    output.append(f"DISCREPANCY: £{float(jan4_csv['Gross sales'].values[0].replace(',','')) - jan_4['Gross Sales'].values[0] if len(jan_4) > 0 else 0:,.2f}")
output.append("=" * 70)

with open('daily_chart_verification.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Results saved to daily_chart_verification.txt")
