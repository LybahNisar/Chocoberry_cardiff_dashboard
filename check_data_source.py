import pandas as pd

# Load the current CSV
df = pd.read_csv('data/raw/chocoberry_cardiff/sales_data.csv', nrows=5)

print("="*80)
print("COLUMNS IN YOUR CURRENT DASHBOARD CSV")
print("="*80)
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

print("\n" + "="*80)
print("COLUMNS YOU SEE IN FLIPDISH 'VIEW SALES'")
print("="*80)
flipdish_view_sales_columns = [
    "sale date", "sale time", "order number", "sequence number", 
    "property name", "store front", "venue code", "dispatch type", 
    "operator", "channel", "retail order price", "discount", 
    "sale refund", "net order price", "charge", "charge refund", 
    "net charge", "net sale price", "net retail vat", "net charge vat", 
    "net sale price include vat", "cash refund", "net cash receipt", 
    "credit refund", "balance", "free amount"
]

for i, col in enumerate(flipdish_view_sales_columns, 1):
    print(f"{i}. {col}")

print("\n" + "="*80)
print("COMPARISON")
print("="*80)

current_cols_lower = [col.lower() for col in df.columns]
flipdish_cols_lower = [col.lower() for col in flipdish_view_sales_columns]

# Check if similar
if 'gross sales' in current_cols_lower:
    print("✅ Your CSV has 'Gross sales' - This looks like SALES SUMMARY format")
elif 'retail order price' in current_cols_lower:
    print("⚠️ Your CSV has 'retail order price' - This looks like DETAILED SALES format")
else:
    print("❓ Unable to determine format")

print("\nYour CSV appears to be from: SALES SUMMARY REPORT")
print("Flipdish 'View Sales' shows: DETAILED TRANSACTION DATA")
print("\n" + "="*80)
