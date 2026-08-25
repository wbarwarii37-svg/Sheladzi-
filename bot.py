import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ========== ڕێکخستنەکان ==========
API_ID = 33774652
API_HASH = "c438941d8f43a0ff59fcc4b3f3c2fb42"

# 🔴 سێشنەکەت (هەمان دوایین دانە)
SESSION_STRING = "1AZWarzgBuyCyj8c2ma6tF7RdpXUH89YLsev7Vpm5tk7WFP_s8k5eqa517QhiOqwbwDMrA9GWOz1nu0fFdsmNhYTfJSAN4lZrC2HusHff-ZcB3gQz6L9SuMZa-POX-rdtA7vZb35B1x8hLoDo18xK6jdvA7iEBGrFfQlA5RG3_65EkikA24ZMIQggek5eDkOBt6aIgpsZC5xSwlxstsMxSC2QiPoyqQSsts7vGQHlJQYvAs7_pCW42ZyF_E7UkBIg0rIEJ7odgs9Fi1_8A0mlOsIblU8H0tLIu3CaoI20XHXgz6shFxE7sCOh5Yc8QUGkVFBNkmY6BAz65XInIHi-fivB9LnvANc="

SOURCE_CHANNEL = "@AdvancedScraper"   # سەرچاوە
TARGET_CHANNEL = "@Cc428Card"         # ئامانج
# ========================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL, from_users='@CC_posterBOT'))
async def handler(event):
    msg = event.message
    new_text = msg.text or ""

    # 🚫 هەموو گۆڕینی ناوەکان لابران (بەبێ replace)

    try:
        if new_text.strip() != "":
            # ناردنی پەیام بە هەمان دەق و فۆرمات (بەبێ گۆڕین)
            await client.send_message(TARGET_CHANNEL, new_text, formatting_entities=msg.entities)
            print(f"✅ پەیام نێردرا بۆ @Cc428Card!")
    except Exception as e:
        print(f"❌ کێشە لە ناردندا: {e}")

async def main():
    try:
        print("Bot is starting up...")
        await client.start()
        print("Bot is now ONLINE! (Forwarding messages from @AdvancedScraper (by @CC_posterBOT) to @Cc428Card without any text modifications)")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Bot disconnected due to network error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
