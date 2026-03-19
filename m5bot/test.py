from libs.m5config import M5config
from libs.m5bot import M5bot
from libs.m5mysql import M5mysql

config = M5config()
bot = config.get("bot")
print(bot["token"])

bot = M5bot()
msg ="mensaje con clases"
bot.send_message(msg)

mysql = M5mysql()
sql = "select * from productos_abarrotes limit 5"
print(mysql.query(sql))