import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
from inspect_csv import inspect_csv

# Load environment variables
load_dotenv()

def process_csv_to_supabase():
    try:
        # Get Supabase credentials
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Get the processed dataframe from inspect_csv
        df = inspect_csv()
        
        if df is None:
            return False
            
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        # Insert data into Supabase
        result = supabase.table('wallet_transactions').insert(records).execute()
        
        print(f"Successfully uploaded {len(records)} transactions to Supabase")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    process_csv_to_supabase() 