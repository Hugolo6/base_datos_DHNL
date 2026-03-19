import requests
from libs.m5config import M5config


class M5bot:
    def __init__(self):
        config = M5config()
        bot = config.get("bot")
        self.token = bot["token"]
        self.chat_id = bot["chat_id"]
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message):
        params = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.get(self.url, params=params)
        print("status:", response.status_code)
        print("Respuesta:", response.json())
        return response.status_code == 200
