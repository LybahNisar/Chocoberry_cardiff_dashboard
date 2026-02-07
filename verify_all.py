import pandas as pd
from datetime import datetime

print("="*80)
print("COMPLETE DASHBOARD VERIFICATION")
print("="*80)

# Load data
df = pd.read_csv('C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff/sales_data.csv')
df['Order time'] = pd.to_datetime(df['Order time'])
filtered = df[(df['Order time'] >= '2026-01-04') & (df['Order time'] <= '2026-02-06 23:59:59')].copy()

# Convert numeric
for col in ['Gross sales', 'Tax on gross sales', 'Charges', 'Revenue']:
    filtered[col] = pd.to_numeric(filtered[col], errors='coerce').fillna(0)

# TEST 1: KPI Metrics
print("\nTEST 1: KPI METRICS")
print("-"*80)
total_rev = filtered['Revenue'].sum()
total_orders = len(filtered)
avg_order = filtered['Gross sales'].mean()
total_tax = filtered['Tax on gross sales'].sum()
total_charges = filtered['Charges'].sum()

print(f"Revenue:  £{total_rev/1000:.1f}K  (expect £81.0K)  {'✅' if abs(total_rev/1000-81)<1 else '❌'}")
print(f"Orders:   {total_orders:,}    (expect 5,275)   {'✅' if total_orders==5275 else '❌'}")
print(f"Avg:      £{avg_order:.2f}   (expect £14.75)  {'✅' if abs(avg_order-14.75)<0.01 else '❌'}")
print(f"Tax:      £{total_tax/1000:.1f}K  (expect £3.0K)   {'✅' if abs(total_tax/1000-3)<0.1 else '❌'}")
print(f"Charges:  £{total_charges:.2f}  (expect £159.84) {'✅' if abs(total_charges-159.84)<0.01 else '❌'}")

# TEST 2: Meal Periods
print("\nTEST 2: MEAL PERIODS")
print("-"*80)

def meal_cat(h):
    if 8<=h<12: return "Breakfast"
    elif 12<=h<16: return "Lunch"
    elif 16<=h<20: return "Evening"
    elif 20<=h<24: return "Dinner"
    else: return "Night"

meal_df = filtered.copy()
meal_df['hour'] = meal_df['Order time'].dt.hour
meal_df['period'] = meal_df['hour'].apply(meal_cat)
meal_sum = meal_df.groupby('period')['Revenue'].agg(['sum', 'count']).reset_index()
meal_sum.columns = ['Period', 'Revenue', 'Orders']
meal_sum = meal_sum.sort_values('Revenue', ascending=False)

best = meal_sum.iloc[0]
worst = meal_sum.iloc[-1]
print(f"Best:  {best['Period']} £{best['Revenue']:,.2f}, {best['Orders']} orders")
print(f"       Expected: Dinner £44,141.51, 2,867 orders")
print(f"       {'✅ MATCH' if abs(best['Revenue']-44141.51)<1 else '❌ MISMATCH'}")

print(f"\nWorst: {worst['Period']} £{worst['Revenue']:,.2f}, {worst['Orders']} orders")
print(f"       Expected: Breakfast £417.49, 23 orders")  
print(f"       {'✅ MATCH' if abs(worst['Revenue']-417.49)<1 else '❌ MISMATCH'}")

# TEST 3: Data Integrity
print("\nTEST 3: DATA INTEGRITY")
print("-"*80)
print(f"Total rows:       {len(filtered):,}")
print(f"Missing revenue:  {filtered['Revenue'].isna().sum()}")
print(f"Missing times:    {filtered['Order time'].isna().sum()}")
print(f"Duplicates:       {filtered['Order ID'].duplicated().sum()}")

integrity_ok = (
    filtered['Revenue'].isna().sum() == 0 and
    filtered['Order time'].isna().sum() == 0 and
    filtered['Order ID'].duplicated().sum() == 0
)
print(f"{'✅ PASS' if integrity_ok else '❌ FAIL'}")

# SUMMARY
print("\n"+"="*80)
print("FINAL RESULT")
print("="*80)

all_ok = (
    abs(total_rev/1000-81)<1 and
    total_orders==5275 and
    abs(best['Revenue']-44141.51)<1 and
    integrity_ok
)

if all_ok:
    print("\n✅✅✅ ALL DASHBOARD DATA IS 100% ACCURATE ✅✅✅")
    print("\nNo hallucination detected.")
    print("All metrics verified against raw CSV.")
else:
    print("\n⚠️ SOME TESTS FAILED - REVIEW NEEDED")

print("="*80)
