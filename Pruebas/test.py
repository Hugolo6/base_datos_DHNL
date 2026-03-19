import libs.M5config
import libs.m5bot
from libs.m5bot import M5bot
from libs.m5config import M5config

config = M5config()
bot = config.get("bot")
print(bot["token"])