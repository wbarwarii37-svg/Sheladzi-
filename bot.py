import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = 33774652
API_HASH = "c438941d8f43a0ff59fcc4b3f3c2fb42"
SESSION_STRING = "1AZWarzgBuyCyj8c2ma6tF7RdpXUH89YLsev7Vpm5tk7WFP_s8k5eqa517QhiOqwbwDMrA9GWOz1nu0fFdsmNhYTfJSAN4lZrC2HusHff-ZcB3gQz6L9SuMZa-POX-rdtA7vZb35B1x8hLoDo18xK6jdvA7iEBGrFfQlA5RG3_65EkikA24ZMIQggek5eDkOBt6aIgpsZC5xSwlxstsMxSC2QiPoyqQSsts7vGQHlJQYvAs7_pCW42ZyF_E7UkBIg0rIEJ7odgs9Fi1_8A0mlOsIblU8H0tLIu3CaoI20XHXgz6shFxE7sCOh5Yc8QUGkVFBNkmY6BAz65XInIHi-fivB9LnvANc="

SOURCE_CHANNEL = "@AdvancedScraper"   # سەرچاوە
TARGET_CHANNEL = "@Cc428Card"         # ئامانج

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        # فۆرواردی هەموو جۆرە پەیامێک (تەکست + میدیا)
        await client.forward_messages(TARGET_CHANNEL, event.message)
        print(f"✅ پەیام فۆروارد کرا بۆ @Cc428Card!")
    except Exception as e:
        print(f"❌ کێشە: {e}")

async def main():
    await client.start()
    print("بۆت کاردەکات! هەموو پەیامەکان دەنێردرێن.")
    await client.run_until_disconnected()

asyncio.run(main())
