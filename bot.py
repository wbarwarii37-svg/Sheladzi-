import asyncio
import re
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== ڕێکخستنەکان ==================
API_ID = 33774652
API_HASH = "c438941d8f43a0ff59fcc4b3f3c2fb42"
SESSION_STRING = "1AZWarzgBuyCyj8c2ma6tF7RdpXUH89YLsev7Vpm5tk7WFP_s8k5eqa517QhiOqwbwDMrA9GWOz1nu0fFdsmNhYTfJSAN4lZrC2HusHff-ZcB3gQz6L9SuMZa-POX-rdtA7vZb35B1x8hLoDo18xK6jdvA7iEBGrFfQlA5RG3_65EkikA24ZMIQggek5eDkOBt6aIgpsZC5xSwlxstsMxSC2QiPoyqQSsts7vGQHlJQYvAs7_pCW42ZyF_E7UkBIg0rIEJ7odgs9Fi1_8A0mlOsIblU8H0tLIu3CaoI20XHXgz6shFxE7sCOh5Yc8QUGkVFBNkmY6BAz65XInIHi-fivB9LnvANc="

SOURCE_CHANNEL = "@AdvancedScraper"   # ✅ سەرچاوە (هەمان ناوی ڕاستەقینە)
TARGET_CHANNEL = "@Cc428Card"         # ✅ ئامانج (چەنالەکەی خۆت)
# ====================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def clean_text(text):
    """ستێرەکان و هێما زیادەکان لادەبات"""
    # لابردنی هەموو ستێرەکان (*)
    text = text.replace("*", "")
    # لابردنی ئەو کاراکتەرەی کە لە دوای ئەعداددا هەیه (وەک 626`)
    text = re.sub(r"(\d+)`", r"\1", text)
    # پاککردنەوەی بۆشایی زیادە
    text = re.sub(r"\s+", " ", text).strip()
    return text

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    try:
        original_text = msg.text or ""
        cleaned_text = clean_text(original_text)
        entities = msg.entities
        media = msg.media

        if media:
            file_path = await client.download_media(media)
            if file_path:
                await client.send_file(
                    TARGET_CHANNEL,
                    file_path,
                    caption=cleaned_text,
                    formatting_entities=entities
                )
                os.remove(file_path)
                print("✅ پەیام (میدیا + تەکستی پاڵێوراو) نێردرا.")
            else:
                if cleaned_text.strip():
                    await client.send_message(TARGET_CHANNEL, cleaned_text, formatting_entities=entities)
                    print("✅ تەکستی پاڵێوراو نێردرا (بەبێ میدیا).")
        else:
            if cleaned_text.strip():
                await client.send_message(TARGET_CHANNEL, cleaned_text, formatting_entities=entities)
                print("✅ پەیامی تەکستی پاڵێوراو نێردرا.")
    except Exception as e:
        print(f"❌ هەڵە: {e}")

async def main():
    await client.start()
    print("🚀 بۆت کاردەکات! پەیامەکان لە @AdvancedScraper کۆپی دەکرێن و ستێرەکان لادەبرێن.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
