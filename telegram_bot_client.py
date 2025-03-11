from telethon.sync import TelegramClient
from telethon import events
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials - Replace with your own
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Bot details
BOT_USERNAME = os.getenv('BOT_USERNAME')

class TelegramBotClient:
    def __init__(self):
        self.client = TelegramClient('session_name', API_ID, API_HASH)
        
    async def start(self):
        """Start the client and connect to Telegram"""
        await self.client.start(phone=PHONE_NUMBER)
        print("Connected to Telegram")
        
    async def send_command_and_get_file(self, token: str, wait_time: int = 25):
        """
        Send a token command to the bot and wait for file response
        """
        try:
            print(f"Sending token command: {token}")
            await self.client.send_message(BOT_USERNAME, token)
            
            print("Waiting for account info...")
            await asyncio.sleep(15)  # Increased wait time for account info
            
            # Check for rate limit message
            messages = await self.client.get_messages(BOT_USERNAME, limit=1)
            if messages and "limit of 3 requests per day" in messages[0].text:
                print("Rate limit reached: You have reached the limit of 3 requests per day!")
                return None
            
            # Find and click the "Download CSV" button with retries
            print("Looking for Download CSV button...")
            button_found = False
            retries = 3
            
            while retries > 0 and not button_found:
                print(f"Searching for button (attempt {4-retries}/3)...")
                async for message in self.client.iter_messages(BOT_USERNAME, limit=20):  # Increased limit
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Download CSV" in button.text:
                                    print("Found Download CSV button, clicking...")
                                    await button.click()
                                    button_found = True
                                    break
                            if button_found:
                                break
                    if button_found:
                        break
                
                if not button_found:
                    print(f"Button not found, waiting 5 seconds before retry...")
                    await asyncio.sleep(5)
                    retries -= 1
            
            if not button_found:
                print("Could not find Download CSV button after all retries")
                return None
            
            # Wait for the file message
            print(f"Button clicked, waiting for file message...")
            await asyncio.sleep(10)  # Increased wait time for file
            
            # Get the file message with retries
            file_found = False
            retries = 3
            
            while retries > 0 and not file_found:
                print(f"Checking for file (attempt {4-retries}/3)...")
                messages = await self.client.get_messages(BOT_USERNAME, limit=5)
                
                for message in messages:
                    if message.file:
                        print("Found file message")
                        # Create downloads directory if it doesn't exist
                        downloads_dir = "downloads"
                        os.makedirs(downloads_dir, exist_ok=True)
                        
                        # Generate filename with timestamp
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"downloads/response_{timestamp}.csv"
                        
                        # Download the file
                        print(f"Downloading file to: {filename}")
                        await message.download_media(filename)
                        
                        # Verify file exists and has content
                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            print(f"File successfully downloaded: {filename}")
                            return filename
                        
                        file_found = True
                        break
                
                if not file_found:
                    print(f"File not found, waiting 5 seconds before retry...")
                    await asyncio.sleep(5)
                    retries -= 1
            
            if not file_found:
                print("Could not find file message after all retries")
                return None
            
        except Exception as e:
            print(f"Error in send_command_and_get_file: {str(e)}")
            return None
            
    async def close(self):
        """Close the client connection"""
        await self.client.disconnect() 