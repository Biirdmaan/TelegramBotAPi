from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    try:
        # Get Supabase credentials
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to fetch something simple to test connection
        response = supabase.table('wallet_transactions').select("*").limit(1).execute()
        
        print("✅ Successfully connected to Supabase!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 