import pandas as pd
import os
from datetime import datetime

def inspect_csv(csv_path=None):
    try:
        # If no specific path is provided, find the most recent CSV in downloads folder
        if not csv_path:
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                print(f"Error: Downloads directory '{downloads_dir}' not found")
                return None
                
            # Get the most recent CSV file
            files = [f for f in os.listdir(downloads_dir) if f.endswith('.csv')]
            if not files:
                print("Error: No CSV files found in downloads directory")
                return None
                
            csv_path = os.path.join(downloads_dir, sorted(files)[-1])
        
        print(f"Reading CSV file: {csv_path}")
        
        # Skip the header information and read only transaction data
        df = pd.read_csv(csv_path, skiprows=17)
        
        # Define proper column names based on the CSV structure
        columns = [
            'token_name',
            'token_address',
            'status',
            'roi_percentage',
            'profit_sol',
            'first_buy',
            'last_sell',
            'buy_txns',
            'sell_txns',
            'tokens_bought',
            'tokens_sold',
            'pre_sale',
            'sold_bought',
            'didnt_buy',
            'snipes'
        ]
        
        # Assign proper column names
        df.columns = columns
        
        # Clean the data
        df = df.dropna(how='all')
        
        print("\nCSV Structure after cleaning:")
        print("--------------")
        print(f"Number of transactions: {len(df)}")
        print("\nColumns:")
        for col in df.columns:
            print(f"- {col}")
        
        print("\nFirst few transactions:")
        print(df.head(3))
        
        return df
        
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return None

if __name__ == "__main__":
    inspect_csv() 