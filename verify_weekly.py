import pandas as pd

# Load sales data
sales_df = pd.read_csv(r"C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\sales_data.csv")
sales_df['Order time'] = pd.to_datetime(sales_df['Order time'])

# Convert numeric columns
sales_df['Gross sales'] = pd.to_numeric(sales_df['Gross sales'], errors='coerce').fillna(0)

# Extract day of week
sales_df['Day of Week'] = sales_df['Order time'].dt.day_name()

# Group by day of week
day_sales = sales_df.groupby('Day of Week')['Gross sales'].sum()
day_orders = sales_df.groupby('Day of Week').size()

# Order by days of week (Monday to Sunday)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_sales = day_sales.reindex(day_order)
day_orders = day_orders.reindex(day_order)

# Get top 3 busiest days
top_days = day_sales.sort_values(ascending=False).head(3)

output = []
output.append("WEEKLY PATTERN VERIFICATION")
output.append("=" * 70)
output.append("\nSALES BY DAY OF WEEK:")
output.append("-" * 70)
for day in day_order:
    if pd.notna(day_sales[day]):
        output.append(f"{day:12} £{day_sales[day]:>10,.2f}  ({day_orders[day]:>4} orders)")

output.append("\n" + "=" * 70)
output.append("BUSIEST DAYS (Top 3):")
output.append("-" * 70)
for i, (day, sales) in enumerate(top_days.items(), 1):
    output.append(f"{i}. {day:12} £{sales:>10,.2f}  ({day_orders[day]:>4} orders)")

output.append("\n" + "=" * 70)
output.append("DASHBOARD SHOWS (from your screenshot):")
output.append("-" * 70)
output.append("Busiest Days:")
output.append("  1. Sunday:   £13,474.43 (898 orders)")
output.append("  2. Saturday: £12,869.64 (871 orders)")
output.append("  3. Friday:   £11,482.93 (778 orders)")
output.append("\nBar Chart (approx readings):")
output.append("  Monday:    ~10k")
output.append("  Tuesday:   ~10k")
output.append("  Wednesday: ~8k")
output.append("  Thursday:  ~8k")
output.append("  Friday:    ~12k")
output.append("  Saturday:  ~13k")
output.append("  Sunday:    ~13k")
output.append("=" * 70)

with open('weekly_pattern_verification.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Saved to weekly_pattern_verification.txt")
