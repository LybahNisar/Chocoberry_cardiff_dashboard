"""
Data Quality Validation Script
Analyzes all CSV files and generates a detailed quality report
"""

import pandas as pd
import os
from pathlib import Path

# Define data directory
DATA_DIR = Path(__file__).parent.parent / 'data' / 'raw' / 'chocoberry_cardiff'

print("=" * 80)
print("📊 DATA QUALITY VALIDATION REPORT")
print("=" * 80)
print()

# List of all CSV files to check
csv_files = [
    'sales_data.csv',
    'sales_overview.csv',
    'gross_sales_per_day.csv',
    'gross_sales_by_dispatch_type.csv',
    'gross_sales_by_hour_of_day.csv',
    'gross_sales_by_payment_method.csv',
    'gross_sales_by_sales_channel.csv',
    'gross_sales_per_day_of_week.csv',
    'revenue_after_refunds.csv',
    'revenue_summary.csv',
    'charges_summary.csv',
    'total_charges.csv'
]

results = {}

print("📁 CHECKING FILES...")
print("-" * 80)

for filename in csv_files:
    filepath = DATA_DIR / filename
    
    if not filepath.exists():
        print(f"❌ {filename}: FILE NOT FOUND")
        continue
    
    try:
        # Read CSV
        df = pd.read_csv(filepath)
        
        # Collect statistics
        stats = {
            'rows': len(df),
            'columns': len(df.columns),
            'file_size_kb': round(filepath.stat().st_size / 1024, 2),
            'null_count': df.isnull().sum().sum(),
            'null_percentage': round((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
            'duplicates': df.duplicated().sum(),
            'status': '✅ CLEAN'
        }
        
        # Determine status
        if stats['null_percentage'] > 50:
            stats['status'] = '❌ HIGH NULL VALUES'
        elif stats['null_percentage'] > 20:
            stats['status'] = '⚠️ MODERATE NULL VALUES'
        
        results[filename] = stats
        
        print(f"✅ {filename}")
        print(f"   Rows: {stats['rows']:,} | Columns: {stats['columns']} | Size: {stats['file_size_kb']} KB")
        print(f"   Null values: {stats['null_count']:,} ({stats['null_percentage']}%) | Duplicates: {stats['duplicates']}")
        print()
        
    except Exception as e:
        print(f"❌ {filename}: ERROR - {str(e)}")
        print()

# Detailed check on main sales_data.csv
print("=" * 80)
print("🔍 DETAILED ANALYSIS: sales_data.csv")
print("=" * 80)

try:
    sales_df = pd.read_csv(DATA_DIR / 'sales_data.csv')
    
    print(f"\n📊 Basic Information:")
    print(f"   Total Transactions: {len(sales_df):,}")
    print(f"   Date Range: {sales_df['Order time'].min()} to {sales_df['Order time'].max()}")
    print(f"   Total Revenue: £{sales_df['Revenue'].sum():,.2f}")
    
    print(f"\n📋 Column-by-Column Null Values:")
    null_counts = sales_df.isnull().sum()
    for col in sales_df.columns:
        null_count = null_counts[col]
        null_pct = (null_count / len(sales_df)) * 100
        if null_count > 0:
            print(f"   ⚠️ {col}: {null_count:,} nulls ({null_pct:.1f}%)")
        else:
            print(f"   ✅ {col}: No nulls")
    
    print(f"\n💰 Revenue Statistics:")
    print(f"   Mean transaction: £{sales_df['Gross sales'].mean():.2f}")
    print(f"   Median transaction: £{sales_df['Gross sales'].median():.2f}")
    print(f"   Min transaction: £{sales_df['Gross sales'].min():.2f}")
    print(f"   Max transaction: £{sales_df['Gross sales'].max():.2f}")
    
    print(f"\n📦 Dispatch Type Breakdown:")
    print(sales_df['Dispatch type'].value_counts().to_string())
    
    print(f"\n💳 Payment Method Breakdown:")
    print(sales_df['Payment method'].value_counts().to_string())
    
    print(f"\n🏪 Sales Channel Breakdown:")
    print(sales_df['Sales channel type'].value_counts().to_string())
    
except Exception as e:
    print(f"❌ Error analyzing sales_data.csv: {str(e)}")

# Summary
print("\n" + "=" * 80)
print("📋 SUMMARY")
print("=" * 80)

total_files = len(csv_files)
checked_files = len(results)
clean_files = sum(1 for r in results.values() if r['status'] == '✅ CLEAN')

print(f"\n✅ Files checked: {checked_files}/{total_files}")
print(f"✅ Clean files: {clean_files}/{checked_files}")
print(f"✅ Total rows across all files: {sum(r['rows'] for r in results.values()):,}")

if clean_files == checked_files:
    print("\n🎉 ALL FILES ARE CLEAN AND READY FOR DASHBOARD DEVELOPMENT!")
else:
    print(f"\n⚠️ {checked_files - clean_files} files need attention")

print("\n" + "=" * 80)
print("✅ Validation complete!")
print("=" * 80)
