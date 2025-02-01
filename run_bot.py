import asyncio
from telegram_bot_client import TelegramBotClient

async def main():
    client = TelegramBotClient()
    try:
        await client.start()
        
        # Get token from user input
        token = input("Please enter the token (e.g. 6apFFc4ydTtb1uWLK5SZ1JgWHY2L6Ajvw8eaiJFBFRfV): ")
        
        # Send token command with 25 second wait time
        result = await client.send_command_and_get_file(token, wait_time=25)  # Changed to 25 seconds
        
        if result:
            print(f"Success! File downloaded to: {result}")
        else:
            print("Failed to get file from bot")
            
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 