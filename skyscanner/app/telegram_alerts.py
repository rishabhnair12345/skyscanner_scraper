import requests
import os

from dotenv import load_dotenv
load_dotenv()

class TelegramNotifier:
    def __init__(self):
        
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id =  os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    def send_alert(self, message):
        """Send message to Telegram channel"""
        endpoint = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Telegram notification failed: {str(e)}")
            return False

def test_telegram_connection():
    notifier = TelegramNotifier()
    return notifier.send_alert("🚀 Flight Alert System Connected Successfully!")