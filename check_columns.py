import pandas as pd
data_path = 'data/raw/chocoberry_cardiff/sales_data.csv'
try:
    df = pd.read_csv(data_path, nrows=5)
    print("Columns:", list(df.columns))
    # Print the first row to see what kind of data is there
    print("Row 0:", df.iloc[0].to_dict())
except Exception as e:
    print(e)
