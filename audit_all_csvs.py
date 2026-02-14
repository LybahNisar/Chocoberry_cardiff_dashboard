import pandas as pd
import glob
import os

# Define the directory
directory = r'C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff'

# Get all CSV files
csv_files = glob.glob(os.path.join(directory, "*.csv"))

print(f"Checking {len(csv_files)} files in {directory}...\n")

for file_path in csv_files:
    filename = os.path.basename(file_path)
    print(f"--- File: {filename} ---")
    try:
        # Read just the first few rows to peek at columns
        df = pd.read_csv(file_path, nrows=2)
        print(f"Columns: {list(df.columns)}")
        
        # Check for keywords indicating item-level data
        item_keywords = ['item', 'product', 'menu', 'qty', 'quantity', 'name']
        found_keywords = [col for col in df.columns if any(k in col.lower() for k in item_keywords)]
        
        if found_keywords:
             print(f"⚠️ POTENTIAL ITEM DATA? Found columns: {found_keywords}")
             # Let's print the first row values for these columns to be sure
             print(f"First Row Data: {df.iloc[0].to_dict()}")
        else:
             print("No item-level columns found.")
             
        # Check row count (fast method for large files)
        with open(file_path, 'r') as f:
            row_count = sum(1 for row in f)
        print(f"Total Rows: {row_count}")
        
    except Exception as e:
        print(f"Error reading file: {e}")
    print("\n")
