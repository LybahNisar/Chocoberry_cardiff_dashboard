"""
Database Setup & Migration Script
=================================
1. Creates a local SQLite database (restaurant_data.db).
2. Defines the 'orders' table schema.
3. Imports the existing 'sales_data.csv' into the database.
4. Handles deduplication (Order ID is the primary key).
"""

import sqlite3
import pandas as pd
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = Path('restaurant_data.db')
CSV_PATH = Path('data/raw/chocoberry_cardiff/sales_data.csv')

def create_schema(conn):
    """Create the orders table if it doesn't exist."""
    cursor = conn.cursor()
    
    # We create a table with ALL columns from your CSV + API essentials
    # Using 'Order ID' as PRIMARY KEY ensures no duplicates ever
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        order_time TIMESTAMP,
        property_name TEXT,
        gross_sales REAL,
        tax REAL,
        tips REAL,
        delivery_charges REAL,
        service_charges REAL,
        additional_charges REAL,
        charges REAL,
        revenue REAL,
        refunds REAL,
        discounts REAL,
        dispatch_type TEXT,
        payment_method TEXT,
        sales_channel_type TEXT,
        sales_channel_name TEXT,
        is_preorder TEXT,
        status TEXT,
        raw_json TEXT
    )
    ''')
    
    # Create an items table for the item-level analysis
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        order_time TIMESTAMP,
        item_name TEXT,
        category TEXT,
        price REAL,
        quantity INTEGER,
        revenue REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )
    ''')
    conn.commit()

def import_csv_to_db(conn):
    """Import the existing CSV history into the DB."""
    if not CSV_PATH.exists():
        logging.error(f"CSV not found at {CSV_PATH}")
        return

    logging.info(f"Reading CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    
    # Data Cleaning (same logic as dashboard)
    # Convert dates
    df['Order time'] = pd.to_datetime(df['Order time'])
    
    # Clean numeric columns
    numeric_columns = ['Gross sales', 'Tax on gross sales', 'Tips', 'Delivery charges', 
                      'Service charges', 'Additional charges', 'Charges', 'Revenue', 
                      'Refunds', 'Discounts']
    
    for col in numeric_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # Insert records
    cursor = conn.cursor()
    count = 0
    skipped = 0
    
    for _, row in df.iterrows():
        try:
            # Map CSV columns to DB columns
            order_id = str(row['Order ID'])
            
            # Use REPLACE INTO or INSERT OR IGNORE to handle duplicates
            # We use INSERT OR IGNORE because CSV data is 'ground truth' for history
            cursor.execute('''
            INSERT OR IGNORE INTO orders (
                order_id, order_time, property_name, gross_sales, tax, tips,
                delivery_charges, service_charges, additional_charges, charges,
                revenue, refunds, discounts, dispatch_type, payment_method,
                sales_channel_type, sales_channel_name, is_preorder
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order_id,
                row['Order time'].isoformat(),
                row.get('Property name', 'Chocoberry Cardiff'),
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
            else:
                skipped += 1
                
        except Exception as e:
            logging.error(f"Error inserting row {row['Order ID']}: {e}")
            
    conn.commit()
    logging.info(f"Import complete. Imported {count} new orders. Skipped {skipped} duplicates.")

def main():
    logging.info(f"Initializing database at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    logging.info("Creating schema...")
    create_schema(conn)
    
    logging.info("Importing legacy CSV data...")
    import_csv_to_db(conn)
    
    # Verify count
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), MIN(order_time), MAX(order_time) FROM orders")
    row = cursor.fetchone()
    logging.info(f"DATABASE STATUS: {row[0]} orders total.")
    logging.info(f"Date Range: {row[1]} to {row[2]}")
    
    conn.close()

if __name__ == "__main__":
    main()
