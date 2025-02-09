import pandas as pd

def inspect_csv():
    try:
        csv_path = "downloads/response_20250209_112235.csv"
        
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