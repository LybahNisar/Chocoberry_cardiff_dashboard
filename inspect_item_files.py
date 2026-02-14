import pandas as pd
import os

files_to_check = [
    r"data/raw/chocoberry_cardiff/best-selling_categories.csv",
    r"data/raw/chocoberry_cardiff/least_sold_items.csv",
    r"data/raw/chocoberry_cardiff/least_sold_item_modifiers.csv",
    r"data/raw/chocoberry_cardiff/most_sold_item_modifiers.csv",
    r"data/raw/chocoberry_cardiff/most_sold_items.csv",
    r"data/raw/chocoberry_cardiff/percentage_increase_in_item_sales.csv",
    r"data/raw/chocoberry_cardiff/refunded_items.csv"
]

print(f"Checking {len(files_to_check)} specific files for item data...\n")

for relative_path in files_to_check:
    file_path = os.path.join(os.getcwd(), relative_path)
    filename = os.path.basename(file_path)
    print(f"--- File: {filename} ---")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
        
    try:
        # Read just the first few rows
        df = pd.read_csv(file_path, nrows=3)
        print(f"Columns: {list(df.columns)}")
        if not df.empty:
            print(f"First Row: {df.iloc[0].to_dict()}")
        else:
            print("File is empty.")
            
    except Exception as e:
        print(f"Error reading file: {e}")
    print("\n")
