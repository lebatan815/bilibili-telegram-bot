import requests
import telebot
import time
from deep_translator import GoogleTranslator

TOKEN = "TOKEN_BOT"
CHAT_ID = "CHAT_ID"

UID_LIST = [
"3493096635463293",
"526977257",
"1204869106",
"3546726409439997",
"3546705395976285",
"10395608835",
"3494365472139115",
"1427119538"
]

bot = telebot.TeleBot(TOKEN)

last_video = {}

def get_avatar(uid):
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
    data = requests.get(url).json()
    return data["data"]["face"]

def check_bilibili(uid):

    url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&pn=1&ps=1"
    data = requests.get(url).json()

    video = data["data"]["list"]["vlist"][0]

    bvid = video["bvid"]
    title = video["title"]
    desc = video["description"]
    pic = video["pic"] + "@1280w_720h"

    link = f"https://www.bilibili.com/video/{bvid}"

    if uid not in last_video or last_video[uid] != bvid:

        last_video[uid] = bvid

        title_vi = GoogleTranslator(source='auto', target='vi').translate(title)
        desc_vi = GoogleTranslator(source='auto', target='vi').translate(desc)

        avatar = get_avatar(uid)

        msg = f"""
🎬 Video mới

Tiêu đề:
{title}

Tiêu đề dịch:
{title_vi}

Mô tả dịch:
{desc_vi}

🔗 {link}
"""

        bot.send_photo(CHAT_ID, avatar)
        bot.send_photo(CHAT_ID, pic, caption=msg)

while True:

    for uid in UID_LIST:
        check_bilibili(uid)

    time.sleep(300)
