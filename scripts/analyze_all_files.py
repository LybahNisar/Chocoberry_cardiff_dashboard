import pandas as pd
from pathlib import Path

print("📊 COMPLETE FILE ANALYSIS\n")
print("="*60)

data_dir = Path('data/raw/chocoberry_cardiff')

files_to_check = [
    'sales_data_old.csv',
    'sales_data.csv', 
    'sales_data_13feb.csv',
    'sales_data_new.csv'
]

all_data = {}

for filename in files_to_check:
    filepath = data_dir / filename
    if filepath.exists():
        df = pd.read_csv(filepath)
        df['Order time'] = pd.to_datetime(df['Order time'], errors='coerce')
        
        # Clean revenue
        if df['Revenue'].dtype == 'object':
            df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')
        
        all_data[filename] = df
        
        print(f"\n📄 {filename}")
        print(f"   Rows: {len(df)}")
        print(f"   Date Range: {df['Order time'].min().date()} to {df['Order time'].max().date()}")
        print(f"   Revenue: £{df['Revenue'].sum():,.2f}")
        print(f"   Unique Order IDs: {df['Order ID'].nunique()}")
    else:
        print(f"\n❌ {filename} - NOT FOUND")

print("\n" + "="*60)
print("\n🔍 OVERLAP ANALYSIS:")

# Check for overlaps between files
if len(all_data) >= 2:
    file_list = list(all_data.keys())
    for i in range(len(file_list)):
        for j in range(i+1, len(file_list)):
            file1 = file_list[i]
            file2 = file_list[j]
            
            ids1 = set(all_data[file1]['Order ID'])
            ids2 = set(all_data[file2]['Order ID'])
            
            overlap = len(ids1 & ids2)
            unique_in_1 = len(ids1 - ids2)
            unique_in_2 = len(ids2 - ids1)
            
            print(f"\n{file1} vs {file2}:")
            print(f"   Overlap: {overlap} orders")
            print(f"   Unique to {file1}: {unique_in_1}")
            print(f"   Unique to {file2}: {unique_in_2}")
