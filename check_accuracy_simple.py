import pandas as pd
from pathlib import Path

# Load data
data_path = Path('data/raw/chocoberry_cardiff')
df = pd.read_csv(data_path / 'sales_data.csv')

# Convert columns EXACTLY as dashboard does
df['Gross sales'] = pd.to_numeric(df['Gross sales'], errors='coerce').fillna(0)
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
df['Order time'] = pd.to_datetime(df['Order time'])

# Filter EXACTLY like dashboard (2026-01-04 to 2026-02-06)
filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06')]

# Calculate metrics EXACTLY as dashboard does
total_orders = len(filtered)
total_revenue = filtered['Revenue'].sum()  # Line 239 of dashboard
avg_order_value = filtered['Gross sales'].mean()  # Line 249 of dashboard

# Write results to file
with open('verification_results.txt', 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("FINAL DASHBOARD VERIFICATION\n")
    f.write("="*70 + "\n\n")
    f.write("DASHBOARD SHOWS (from screenshot):\n")
    f.write("  Total Revenue: GBP 81.0K\n")
    f.write("  Total Orders: 5,275\n")
    f.write("  Average Order Value: GBP 14.75\n\n")
    f.write("CSV CALCULATED VALUES:\n")
    f.write(f"  Total Revenue: GBP {total_revenue/1000:.1f}K (exact: GBP {total_revenue:,.2f})\n")
    f.write(f"  Total Orders: {total_orders:,}\n")
    f.write(f"  Average Order Value: GBP {avg_order_value:.2f}\n\n")
    f.write("="*70 + "\n")
    f.write("VERIFICATION RESULT:\n")
    f.write("="*70 + "\n\n")
    
    all_match = True
    
    if total_orders == 5275:
        f.write("PASS Total Orders: MATCH (5,275)\n")
    else:
        f.write(f"FAIL Total Orders: MISMATCH - CSV={total_orders}, Dashboard=5,275\n")
        all_match = False
    
    revenue_k = total_revenue / 1000
    if abs(revenue_k - 81.0) < 0.1:
        f.write(f"PASS Total Revenue: MATCH (GBP 81.0K)\n")
    else:
        f.write(f"FAIL Total Revenue: MISMATCH - CSV=GBP{revenue_k:.1f}K, Dashboard=GBP81.0K\n")
        all_match = False
    
    if abs(avg_order_value - 14.75) < 0.01:
        f.write(f"PASS Average Order Value: MATCH (GBP 14.75)\n")
    else:
        f.write(f"FAIL Average Order Value: MISMATCH - CSV=GBP{avg_order_value:.2f}, Dashboard=GBP14.75\n")
        all_match = False
    
    f.write("\n")
    if all_match:
        f.write("DASHBOARD IS 100% ACCURATE\n")
    else:
        f.write("DISCREPANCIES FOUND\n")
    f.write("="*70 + "\n")

print("Results written to verification_results.txt")
print(f"Orders: {total_orders}")
print(f"Revenue: GBP{total_revenue/1000:.1f}K")
print(f"AOV: GBP{avg_order_value:.2f}")
