"""
COMPREHENSIVE DASHBOARD AUDIT
Professional Debugging Report
"""

import pandas as pd
from pathlib import Path
import sys

print("=" * 80)
print("COMPREHENSIVE DASHBOARD DATA AUDIT")
print("=" * 80)

errors = []
warnings = []
passed = []

# TEST 1: FILE INTEGRITY
print("\n[TEST 1] FILE INTEGRITY CHECK")
print("-" * 80)

csv_path = Path('data/raw/chocoberry_cardiff/sales_data.csv')

if not csv_path.exists():
    errors.append("CRITICAL: sales_data.csv does not exist")
    print("[FAIL] File not found")
    sys.exit(1)
else:
    passed.append("File exists")
    print(f"[PASS] File exists: {csv_path}")

try:
    df = pd.read_csv(csv_path)
    passed.append(f"File readable ({len(df)} rows)")
    print(f"[PASS] File readable: {len(df)} rows")
except Exception as e:
    errors.append(f"CRITICAL: Cannot read file - {e}")
    print(f"[FAIL] {e}")
    sys.exit(1)

# TEST 2: REQUIRED COLUMNS
print("\n[TEST 2] REQUIRED COLUMNS CHECK")
print("-" * 80)

required_columns = ['Order ID', 'Order time', 'Revenue', 'Gross sales', 'Dispatch type', 'Sales channel type']

for col in required_columns:
    if col in df.columns:
        passed.append(f"Column '{col}' exists")
        print(f"[PASS] Column '{col}' exists")
    else:
        errors.append(f"CRITICAL: Missing column '{col}'")
        print(f"[FAIL] Missing column '{col}'")

# TEST 3: DATE PARSING
print("\n[TEST 3] DATE PARSING CHECK")
print("-" * 80)

try:
    df['Order time'] = pd.to_datetime(df['Order time'], errors='coerce')
    null_dates = df['Order time'].isna().sum()
    
    if null_dates > 0:
        warnings.append(f"{null_dates} rows have invalid dates")
        print(f"[WARN] {null_dates} rows with invalid dates")
    else:
        passed.append("All dates parsed successfully")
        print("[PASS] All dates parsed successfully")
    
    min_date = df['Order time'].min()
    max_date = df['Order time'].max()
    
    print(f"       Date range: {min_date} to {max_date}")
    
except Exception as e:
    errors.append(f"CRITICAL: Date parsing failed - {e}")
    print(f"[FAIL] {e}")

# TEST 4: DATE RANGE VERIFICATION
print("\n[TEST 4] DATE RANGE VERIFICATION")
print("-" * 80)

expected_start = pd.to_datetime('2026-01-04')

if df['Order time'].min().date() == expected_start.date():
    passed.append("Start date correct (2026-01-04)")
    print("[PASS] Start date: 2026-01-04 (CORRECT)")
else:
    errors.append(f"Start date mismatch")
    print(f"[FAIL] Start date: {df['Order time'].min().date()}")

feb_12_data = df[df['Order time'].dt.date == pd.to_datetime('2026-02-12').date()]
if len(feb_12_data) > 100:
    passed.append(f"Feb 12 has complete data ({len(feb_12_data)} orders)")
    print(f"[PASS] Feb 12: {len(feb_12_data)} orders (COMPLETE)")
else:
    warnings.append(f"Feb 12 may be incomplete")
    print(f"[WARN] Feb 12: {len(feb_12_data)} orders")

feb_13_data = df[df['Order time'].dt.date == pd.to_datetime('2026-02-13').date()]
print(f"[INFO] Feb 13: {len(feb_13_data)} orders (INCOMPLETE - EXPECTED)")

# TEST 5: DUPLICATE CHECK
print("\n[TEST 5] DUPLICATE ORDER IDs CHECK")
print("-" * 80)

duplicates = df['Order ID'].duplicated().sum()
if duplicates == 0:
    passed.append("No duplicate Order IDs")
    print("[PASS] No duplicate Order IDs")
else:
    errors.append(f"CRITICAL: {duplicates} duplicate Order IDs")
    print(f"[FAIL] {duplicates} duplicate Order IDs")

# TEST 6: DATA GAPS CHECK
print("\n[TEST 6] DATA GAPS CHECK")
print("-" * 80)

daily_counts = df.groupby(df['Order time'].dt.date).size()
low_days = daily_counts[daily_counts < 50]

if len(low_days) == 0:
    passed.append("No suspicious gaps")
    print("[PASS] No suspicious gaps (all days have 50+ orders)")
elif len(low_days) == 1 and low_days.index[0] == pd.to_datetime('2026-02-13').date():
    passed.append("Only Feb 13 is low (expected)")
    print("[PASS] Only Feb 13 is low (expected)")
else:
    warnings.append(f"{len(low_days)} days with <50 orders")
    print(f"[WARN] {len(low_days)} days with <50 orders")

# TEST 7: REVENUE DATA INTEGRITY
print("\n[TEST 7] REVENUE DATA INTEGRITY")
print("-" * 80)

if df['Revenue'].dtype == 'object':
    df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')
else:
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

null_revenue = df['Revenue'].isna().sum()

if null_revenue > 0:
    warnings.append(f"{null_revenue} rows with null revenue")
    print(f"[WARN] {null_revenue} rows with null revenue")
else:
    passed.append("No null revenue values")
    print("[PASS] No null revenue values")

# TEST 8: STATISTICAL VALIDATION
print("\n[TEST 8] STATISTICAL VALIDATION")
print("-" * 80)

complete_data = df[df['Order time'].dt.date <= pd.to_datetime('2026-02-12').date()]

total_orders = len(complete_data)
total_revenue = complete_data['Revenue'].sum()
avg_order = complete_data['Revenue'].mean()
days = (complete_data['Order time'].max() - complete_data['Order time'].min()).days + 1

print(f"       Total Orders (Jan 4 - Feb 12): {total_orders:,}")
print(f"       Total Revenue: £{total_revenue:,.2f}")
print(f"       Average Order Value: £{avg_order:.2f}")
print(f"       Days of Data: {days}")
print(f"       Average Orders/Day: {total_orders/days:.0f}")

if 6000 <= total_orders <= 7000:
    passed.append(f"Total orders ({total_orders}) is reasonable")
    print(f"[PASS] Total orders is reasonable")
else:
    warnings.append(f"Total orders ({total_orders}) seems unusual")
    print(f"[WARN] Total orders seems unusual")

if 10 <= avg_order <= 30:
    passed.append(f"Average order value is reasonable")
    print(f"[PASS] Average order value is reasonable")
else:
    warnings.append(f"Average order value seems unusual")
    print(f"[WARN] Average order value seems unusual")

# FINAL REPORT
print("\n" + "=" * 80)
print("AUDIT SUMMARY")
print("=" * 80)

print(f"\n[PASS] {len(passed)} checks passed")
print(f"[WARN] {len(warnings)} warnings")
print(f"[FAIL] {len(errors)} critical errors")

if errors:
    print("\nCRITICAL ERRORS:")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")

if warnings:
    print("\nWARNINGS:")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")

print("\n" + "=" * 80)
if len(errors) == 0 and len(warnings) <= 2:
    print("VERDICT: DATA IS READY FOR CLIENT")
    print("  - All critical checks passed")
    print("  - Minor warnings are acceptable")
    print("  - Recommended date range: Jan 4 - Feb 12, 2026")
elif len(errors) == 0:
    print("VERDICT: DATA IS USABLE BUT HAS WARNINGS")
    print("  - No critical errors")
    print("  - Review warnings before sending to client")
else:
    print("VERDICT: DATA HAS CRITICAL ISSUES")
    print("  - DO NOT send to client until errors are fixed")
print("=" * 80)
