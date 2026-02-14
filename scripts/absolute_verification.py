import pandas as pd
from pathlib import Path

print("=" * 60)
print("ABSOLUTE DATA VERIFICATION")
print("=" * 60)

# Load the CSV file
csv_path = Path('data/raw/chocoberry_cardiff/sales_data.csv')
df = pd.read_csv(csv_path)

print(f"\n1. FILE INFO:")
print(f"   File exists: {csv_path.exists()}")
print(f"   Total rows: {len(df)}")
print(f"   Columns: {list(df.columns[:5])}...")

# Parse dates
df['Order time'] = pd.to_datetime(df['Order time'], errors='coerce')

print(f"\n2. DATE RANGE:")
print(f"   Earliest order: {df['Order time'].min()}")
print(f"   Latest order: {df['Order time'].max()}")
print(f"   Total days: {(df['Order time'].max() - df['Order time'].min()).days + 1}")

# Count orders by date
print(f"\n3. ORDERS BY DATE (First 5 and Last 5):")
daily_counts = df.groupby(df['Order time'].dt.date).size().sort_index()
print("\n   First 5 days:")
for date, count in daily_counts.head(5).items():
    print(f"   {date}: {count} orders")
print("\n   Last 5 days:")
for date, count in daily_counts.tail(5).items():
    print(f"   {date}: {count} orders")

# Revenue analysis
print(f"\n4. REVENUE ANALYSIS:")
for col in ['Revenue', 'Gross sales', 'Revenue after refunds']:
    if col in df.columns:
        # Clean the column
        if df[col].dtype == 'object':
            clean_col = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
        else:
            clean_col = pd.to_numeric(df[col], errors='coerce')
        
        total = clean_col.sum()
        print(f"   {col}: £{total:,.2f}")

print(f"\n5. SAMPLE RECENT ORDERS (Last 3):")
recent = df.nlargest(3, 'Order time')[['Order time', 'Order ID', 'Revenue']]
for idx, row in recent.iterrows():
    print(f"   {row['Order time']} - Order {row['Order ID']}: £{row['Revenue']}")

print("\n" + "=" * 60)
