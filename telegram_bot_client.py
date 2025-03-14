from telethon.sync import TelegramClient
from telethon import events
import asyncio
import os
from datetime import datetime
import streamlit as st

# Telegram API credentials from Streamlit secrets
API_ID = st.secrets["API_ID"]
API_HASH = st.secrets["API_HASH"]
PHONE_NUMBER = st.secrets["PHONE_NUMBER"]
BOT_USERNAME = st.secrets["BOT_USERNAME"]

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
        Args:
            token: The token command (e.g. '6apFFc4ydTtb1uWLK5SZ1JgWHY2L6Ajvw8eaiJFBFRfV')
            wait_time: Time to wait for response in seconds
        """
        try:
            print(f"Sending token command: {token}")
            await self.client.send_message(BOT_USERNAME, token)
            
            print(f"Waiting for account info...")
            await asyncio.sleep(5)  # Wait for account info
            
            # Check for rate limit message
            messages = await self.client.get_messages(BOT_USERNAME, limit=1)
            if messages and "limit of 3 requests per day" in messages[0].text:
                print("Rate limit reached: You have reached the limit of 3 requests per day!")
                return None
            
            # Click the "Download CSV" button
            print("Clicking Download CSV button...")
            async for message in self.client.iter_messages(BOT_USERNAME, limit=10):
                if message.buttons:
                    for row in message.buttons:
                        for button in row:
                            if "Download CSV" in button.text:
                                await button.click()
                                break
            
            print(f"Waiting {wait_time} seconds for file...")
            await asyncio.sleep(wait_time)
            
            # Try multiple times to get the file
            for attempt in range(3):
                messages = await self.client.get_messages(BOT_USERNAME, limit=1)
                if messages and messages[0].file:
                    break
                elif messages and "limit of 3 requests per day" in messages[0].text:
                    print("Rate limit reached: You have reached the limit of 3 requests per day!")
                    return None
                elif messages and "Wait 10 seconds before next request" in messages[0].text:
                    print("Rate limit cooldown, waiting 12 seconds...")
                    await asyncio.sleep(12)
                    # Click the button again after cooldown
                    async for message in self.client.iter_messages(BOT_USERNAME, limit=10):
                        if message.buttons:
                            for row in message.buttons:
                                for button in row:
                                    if "Download CSV" in button.text:
                                        await button.click()
                                        break
                print(f"Attempt {attempt + 1}: Waiting for file...")
                await asyncio.sleep(10)
            
            if messages:
                message = messages[0]
                if message.file:
                    # Create downloads directory if it doesn't exist
                    os.makedirs('downloads', exist_ok=True)
                    
                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"downloads/response_{timestamp}{os.path.splitext(message.file.name)[1]}"
                    
                    # Download the file
                    await message.download_media(filename)
                    print(f"File downloaded to: {filename}")
                    return filename
                else:
                    print("No file received in response")
                    return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
            
    async def close(self):
        """Close the client connection"""
        await self.client.disconnect() 