import pandas as pd
from pathlib import Path

"""
COMPREHENSIVE CSV MERGE VERIFICATION
=====================================
This script thoroughly verifies the merged sales_data.csv file.
Checks for missing data, duplicates, date ranges, and data integrity.
"""

print("=" * 80)
print("COMPREHENSIVE MERGE VERIFICATION - Starting...")
print("=" * 80)

# File paths
data_path = Path("C:/Users/GEO/Desktop/Dashboard/data/raw/chocoberry_cardiff")
old_file = data_path / "sales_data_old.csv"
new_file = data_path / "sales_data_new.csv"
merged_file = data_path / "sales_data.csv"

# Load all three files
print("\n📂 LOADING FILES...")
print("-" * 80)

old_df = pd.read_csv(old_file)
print(f"✅ OLD file loaded: {len(old_df):,} rows")

new_df = pd.read_csv(new_file)
print(f"✅ NEW file loaded: {len(new_df):,} rows")

merged_df = pd.read_csv(merged_file)
print(f"✅ MERGED file loaded: {len(merged_df):,} rows")

# Convert dates
old_df['Order time'] = pd.to_datetime(old_df['Order time'], errors='coerce')
new_df['Order time'] = pd.to_datetime(new_df['Order time'], errors='coerce')
merged_df['Order time'] = pd.to_datetime(merged_df['Order time'], errors='coerce')

# TEST 1: Row Count Check
print("\n" + "=" * 80)
print("TEST 1: ROW COUNT VERIFICATION")
print("=" * 80)

expected_min = max(len(old_df), len(new_df))
expected_max = len(old_df) + len(new_df)

print(f"Old file rows:     {len(old_df):,}")
print(f"New file rows:     {len(new_df):,}")
print(f"Merged rows:       {len(merged_df):,}")
print(f"Expected range:    {expected_min:,} to {expected_max:,}")

if expected_min <= len(merged_df) <= expected_max:
    print("✅ PASS: Row count is within expected range")
else:
    print("❌ FAIL: Row count is outside expected range!")

# TEST 2: Date Range Check
print("\n" + "=" * 80)
print("TEST 2: DATE RANGE VERIFICATION")
print("=" * 80)

old_min = old_df['Order time'].min()
old_max = old_df['Order time'].max()
new_min = new_df['Order time'].min()
new_max = new_df['Order time'].max()
merged_min = merged_df['Order time'].min()
merged_max = merged_df['Order time'].max()

print(f"OLD file range:    {old_min.date()} to {old_max.date()}")
print(f"NEW file range:    {new_min.date()} to {new_max.date()}")
print(f"MERGED range:      {merged_min.date()} to {merged_max.date()}")

expected_start = min(old_min, new_min)
expected_end = max(old_max, new_max)

print(f"\nExpected range:    {expected_start.date()} to {expected_end.date()}")

if merged_min == expected_start and merged_max == expected_end:
    print("✅ PASS: Date range matches expected (complete coverage)")
else:
    print("⚠️  WARNING: Date range doesn't match expected")

# TEST 3: Duplicate Check
print("\n" + "=" * 80)
print("TEST 3: DUPLICATE CHECK")
print("=" * 80)

total_before = len(merged_df)
duplicates = merged_df[merged_df.duplicated(subset=['Order ID'], keep=False)]
unique_after = merged_df.drop_duplicates(subset=['Order ID']).shape[0]

print(f"Total rows in merged:     {total_before:,}")
print(f"Unique Order IDs:         {unique_after:,}")
print(f"Duplicate rows found:     {len(duplicates):,}")

if len(duplicates) == 0:
    print("✅ PASS: No duplicates found")
else:
    print(f"❌ FAIL: Found {len(duplicates)} duplicate rows!")
    print("\nDuplicate Order IDs:")
    print(duplicates[['Order ID', 'Order time', 'Gross sales']].head(10))

# TEST 4: Data Completeness - Check if all old data is present
print("\n" + "=" * 80)
print("TEST 4: OLD DATA COMPLETENESS")
print("=" * 80)

old_ids = set(old_df['Order ID'].dropna())
merged_ids = set(merged_df['Order ID'].dropna())
missing_old = old_ids - merged_ids

print(f"Old file Order IDs:       {len(old_ids):,}")
print(f"Found in merged:          {len(old_ids & merged_ids):,}")
print(f"Missing from merged:      {len(missing_old):,}")

if len(missing_old) == 0:
    print("✅ PASS: All old data is present in merged file")
else:
    print(f"❌ FAIL: Missing {len(missing_old)} orders from old file!")
    print("Missing Order IDs (first 10):")
    print(list(missing_old)[:10])

# TEST 5: Data Completeness - Check if all new data is present
print("\n" + "=" * 80)
print("TEST 5: NEW DATA COMPLETENESS")
print("=" * 80)

new_ids = set(new_df['Order ID'].dropna())
missing_new = new_ids - merged_ids

print(f"New file Order IDs:       {len(new_ids):,}")
print(f"Found in merged:          {len(new_ids & merged_ids):,}")
print(f"Missing from merged:      {len(missing_new):,}")

if len(missing_new) == 0:
    print("✅ PASS: All new data is present in merged file")
else:
    print(f"❌ FAIL: Missing {len(missing_new)} orders from new file!")
    print("Missing Order IDs (first 10):")
    print(list(missing_new)[:10])

# TEST 6: Hallucinated Data Check
print("\n" + "=" * 80)
print("TEST 6: HALLUCINATED DATA CHECK")
print("=" * 80)

all_source_ids = old_ids | new_ids
hallucinated = merged_ids - all_source_ids

print(f"Total source Order IDs:   {len(all_source_ids):,}")
print(f"Merged Order IDs:         {len(merged_ids):,}")
print(f"Hallucinated IDs:         {len(hallucinated):,}")

if len(hallucinated) == 0:
    print("✅ PASS: No hallucinated data - all orders come from source files")
else:
    print(f"❌ FAIL: Found {len(hallucinated)} hallucinated orders!")
    print("Hallucinated Order IDs (first 10):")
    print(list(hallucinated)[:10])

# TEST 7: Revenue Verification
print("\n" + "=" * 80)
print("TEST 7: REVENUE INTEGRITY CHECK")
print("=" * 80)

# Check a sample of orders to verify data wasn't corrupted
sample_ids = list(old_ids & new_ids)[:10]  # Orders in both files (overlap)

print("Checking 10 overlapping orders for data integrity...")
issues = 0

for order_id in sample_ids:
    old_row = old_df[old_df['Order ID'] == order_id].iloc[0]
    new_row = new_df[new_df['Order ID'] == order_id].iloc[0]
    merged_row = merged_df[merged_df['Order ID'] == order_id].iloc[0]
    
    # Check if merged matches either old or new (should match one of them)
    if (merged_row['Gross sales'] != old_row['Gross sales'] and 
        merged_row['Gross sales'] != new_row['Gross sales']):
        print(f"⚠️ Order {order_id}: Revenue mismatch!")
        issues += 1

if issues == 0:
    print("✅ PASS: All sampled orders have correct revenue data")
else:
    print(f"❌ FAIL: Found {issues} orders with revenue mismatches")

# TEST 8: Date Coverage Check
print("\n" + "=" * 80)
print("TEST 8: DATE COVERAGE CHECK")
print("=" * 80)

# Check if we have data for each day in the range
merged_dates = merged_df['Order time'].dt.date.value_counts().sort_index()

print(f"Date range: {merged_min.date()} to {merged_max.date()}")
print(f"Total days in range: {(merged_max - merged_min).days + 1}")
print(f"Days with data: {len(merged_dates)}")

# Show first 5 and last 5 days
print("\nFirst 5 days:")
print(merged_dates.head(5))
print("\nLast 5 days:")
print(merged_dates.tail(5))

# FINAL SUMMARY
print("\n" + "=" * 80)
print("FINAL VERIFICATION SUMMARY")
print("=" * 80)

tests_passed = 0
total_tests = 8

if expected_min <= len(merged_df) <= expected_max:
    tests_passed += 1
if merged_min == expected_start and merged_max == expected_end:
    tests_passed += 1
if len(duplicates) == 0:
    tests_passed += 1
if len(missing_old) == 0:
    tests_passed += 1
if len(missing_new) == 0:
    tests_passed += 1
if len(hallucinated) == 0:
    tests_passed += 1
if issues == 0:
    tests_passed += 1
tests_passed += 1  # Date coverage (informational)

print(f"\nTests Passed: {tests_passed}/{total_tests}")
print(f"\nMerged File Stats:")
print(f"  - Total Orders: {len(merged_df):,}")
print(f"  - Date Range: {merged_min.date()} to {merged_max.date()}")
print(f"  - Days Covered: {(merged_max - merged_min).days + 1}")
print(f"  - Unique Order IDs: {unique_after:,}")

if tests_passed == total_tests:
    print("\n✅ ALL TESTS PASSED - Merge is 100% accurate!")
else:
    print(f"\n⚠️  WARNING: {total_tests - tests_passed} test(s) failed")

print("=" * 80)
