"""
Import Historical Data Script
=============================
Use this script to import additional CSV files (e.g., 2025 data) into the database.

Usage:
    1. Download CSV from Flipdish Portal (Orders Export)
    2. Save it to the project folder
    3. Run: py scripts/import_history.py "path/to/your/file.csv"
"""

import sqlite3
import pandas as pd
import sys
import os

DB_PATH = 'restaurant_data.db'

def import_csv(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Reading {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Basic cleaning
    if 'Order time' in df.columns:
        df['Order time'] = pd.to_datetime(df['Order time'])
    
    # Map columns
    numeric_columns = ['Gross sales', 'Tax on gross sales', 'Tips', 'Delivery charges', 
                      'Service charges', 'Revenue', 'Refunds', 'Discounts']
    
    for col in numeric_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    count = 0
    
    print("Importing orders...")
    for _, row in df.iterrows():
        try:
            # Check required column
            if 'Order ID' not in row:
                continue
                
            order_id = str(row['Order ID'])
            
            cursor.execute('''
            INSERT OR IGNORE INTO orders (
                order_id, order_time, property_name, gross_sales, tax, tips,
                delivery_charges, service_charges, additional_charges, charges,
                revenue, refunds, discounts, dispatch_type, payment_method,
                sales_channel_type, sales_channel_name, is_preorder
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order_id,
                row.get('Order time').isoformat() if pd.notnull(row.get('Order time')) else None,
                row.get('Property name', 'Unknown'),
                row.get('Gross sales', 0),
                row.get('Tax on gross sales', 0),
                row.get('Tips', 0),
                row.get('Delivery charges', 0),
                row.get('Service charges', 0),
                row.get('Additional charges', 0),
                row.get('Charges', 0),
                row.get('Revenue', 0),
                row.get('Refunds', 0),
                row.get('Discounts', 0),
                row.get('Dispatch type', 'Unknown'),
                row.get('Payment method', 'Unknown'),
                row.get('Sales channel type', 'Unknown'),
                row.get('Sales channel name', 'Unknown'),
                row.get('Is preorder', 'No')
            ))
            if cursor.rowcount > 0:
                count += 1
        except Exception as e:
            pass # Skip bad rows
            
    conn.commit()
    conn.close()
    print(f"✅ Successfully imported {count} new orders!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the CSV file path.")
        print('Example: py scripts/import_history.py "data/2025_sales.csv"')
    else:
        import_csv(sys.argv[1])
