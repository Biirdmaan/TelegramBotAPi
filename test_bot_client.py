import unittest
import asyncio
from telegram_bot_client import TelegramBotClient

class TestTelegramBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        
    def setUp(self):
        self.client = TelegramBotClient()
        self.loop.run_until_complete(self.client.start())
    
    def tearDown(self):
        self.loop.run_until_complete(self.client.close())
    
    def test_bot_interaction_with_token(self):
        # Example token - replace with a real one for testing
        token = "6apFFc4ydTtb1uWLK5SZ1JgWHY2L6Ajvw8eaiJFBFRfV"
        result = self.loop.run_until_complete(
            self.client.send_command_and_get_file(token)
        )
        self.assertIsNotNone(result, "No file was received from the bot")

if __name__ == '__main__':
    unittest.main() 