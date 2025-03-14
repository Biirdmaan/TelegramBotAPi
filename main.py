import asyncio
import os
from telegram_bot_client import TelegramBotClient
from store_csv_to_supabase import process_csv_to_supabase
import subprocess
import re
import sys

def validate_wallet_address(address):
    """Validate the wallet address format"""
    # Check if it matches the expected length and character pattern
    pattern = r'^[A-Za-z0-9]{44}$'  # 44 characters, alphanumeric
    return bool(re.match(pattern, address))

async def get_wallet_address():
    """Get and validate wallet address from user"""
    while True:
        wallet_address = input("Please enter the wallet address (44 characters): ")
        if validate_wallet_address(wallet_address):
            return wallet_address
        print("Invalid wallet address format. It should be 44 characters long and contain only letters and numbers.")

async def main():
    # Get and validate wallet address
    wallet_address = await get_wallet_address()
    
    # Step 1: Get CSV from Telegram
    client = TelegramBotClient()
    try:
        await client.start()
        print("Requesting CSV from Telegram bot...")
        csv_path = await client.send_command_and_get_file(wallet_address, wait_time=25)
        
        if not csv_path:
            print("Failed to get CSV file. Exiting...")
            return
            
        print(f"Success! CSV downloaded to: {csv_path}")
        
        # Step 2: Store in Supabase with wallet address
        success = process_csv_to_supabase(wallet_address)
        if not success:
            print("Failed to store data in Supabase. Exiting...")
            return
        
        # Step 3: Launch Dashboard
        launch_dashboard()
        
        print("\nApplication is ready!")
        print("1. Data has been stored in Supabase")
        print("2. Dashboard is launching in your default browser")
        print("3. Press Ctrl+C to exit")
        
    finally:
        print("Closing Telegram client...")
        await client.close()

def launch_dashboard():
    print("Launching dashboard...")
    subprocess.Popen(["python", "-m", "streamlit", "run", "dashboard.py"])

def main():
    print("Launching Streamlit Dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])

if __name__ == "__main__":
    main() 