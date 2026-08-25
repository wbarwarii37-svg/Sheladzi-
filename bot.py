import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

# ========== ڕێکخستنەکان ==========
API_ID = 33774652
API_HASH = "c438941d8f43a0ff59fcc4b3f3c2fb42"

SESSION_STRING = "1AZWarzgBuyCyj8c2ma6tF7RdpXUH89YLsev7Vpm5tk7WFP_s8k5eqa517QhiOqwbwDMrA9GWOz1nu0fFdsmNhYTfJSAN4lZrC2HusHff-ZcB3gQz6L9SuMZa-POX-rdtA7vZb35B1x8hLoDo18xK6jdvA7iEBGrFfQlA5RG3_65EkikA24ZMIQggek5eDkOBt6aIgpsZC5xSwlxstsMxSC2QiPoyqQSsts7vGQHlJQYvAs7_pCW42ZyF_E7UkBIg0rIEJ7odgs9Fi1_8A0mlOsIblU8H0tLIu3CaoI20XHXgz6shFxE7sCOh5Yc8QUGkVFBNkmY6BAz65XInIHi-fivB9LnvANc="

SOURCE_CHANNEL = "@AdvancedScraper"   # سەرچاوە
TARGET_CHANNEL = "@Cc428Card"         # ئامانج (چەنالەکەی خۆت)
# ========================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    try:
        text = msg.text or ""
        entities = msg.entities  # بۆ ڕازاندنەوەی تەکست (گرنگ، زیاد، ڕەنگ...)
        media = msg.media

        # ١. ئەگەر میدیا هەبوو (وێنە، ڤیدیۆ، فایل)
        if media:
            # داگرتنی میدیا لەسەر ڕاژە (بە شێوەی کاتی)
            file_path = await client.download_media(media)
            if file_path:
                # ناردنی میدیا وەک پەیامێکی نوێ، لەگەڵ تەکستەکەی
                await client.send_file(
                    TARGET_CHANNEL,
                    file_path,
                    caption=text,  # ناونیشانی پەیام
                    formatting_entities=entities  # پاراستنی ڕازاندنەوە
                )
                # سڕینەوەی فایلە کاتییەکە دوای ناردن (بۆ پاراستنی بۆشایی)
                os.remove(file_path)
                print(f"✅ پەیامی میدیا + تەکست کۆپی کرا و نێردرا!")
            else:
                # ئەگەر داگرتن سەرکەوتوو نەبوو، تەنیا تەکستەکە بنێرە
                if text.strip():
                    await client.send_message(TARGET_CHANNEL, text, formatting_entities=entities)
                    print(f"✅ تەکستەکە نێردرا (بەبێ میدیا)")
        else:
            # ٢. ئەگەر تەنیا تەکست بوو
            if text.strip():
                await client.send_message(TARGET_CHANNEL, text, formatting_entities=entities)
                print(f"✅ پەیامی تەکست کۆپی کرا و نێردرا!")

    except Exception as e:
        print(f"❌ کێشە لە کۆپیکردندا: {e}")

async def main():
    try:
        print("بۆت دەستپێدەکات...")
        await client.start()
        print("✅ بۆت ئێستا کاردەکات! (کۆپی دەکات، نەک فۆروارد)")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"بۆت لە کار کەوت بەهۆی: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
