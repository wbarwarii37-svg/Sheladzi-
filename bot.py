import asyncio
import re
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== ڕێکخستنەکان ==================
API_ID = int(os.getenv("API_ID", 33774652))
API_HASH = os.getenv("API_HASH", "c438941d8f43a0ff59fcc4b3f3c2fb42")
SESSION_STRING = os.getenv("SESSION_STRING", "1AZWarzgBu5kZeJjoXsUl26R4vl8Z7CtKLNbejoE6xJ9IpQJvCcf_vB_X9YhC3WM34WQx9KXFnEVHAKR4Gvg4E7I6wh8hBJ_5UUUqSbljF1hJUqtPKCvvyDY_27OulPpfn_gqY4QQGB8erMherkUCgAOX3jrtHnqV6kECO6BhGk4EN0XLC5VWUvYShY954HPMQV5XkkjR5LwY4q6y5fJwmo1jI_ClIty3KT-Yd85jsDoNuL7zD6L5iYkzP_QDqg_3xa8wZnU6LBNbfMy9hf9jn_LySWuYqBhRMhWc1Sfc39bpSI33W_Xtk47NLFeMmwVPDZv20dLYgQ4m0nDtfNIdUW1BNQ13KgQ=")

SOURCE_CHANNEL = "@AdvancedScraper"   # سەرچاوە
TARGET_CHANNEL = "@Cc428Card"         # ئامانج
# ====================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# فەنکشنی نوێ: پشکنین دەکات ئایا ژمارەی کارت لە پەیامەکەدا هەیە یان نا
def contains_card(text):
    if not text:
        return False
    # بەدوای ژمارەی کارتدا دەگەڕێت (13 بۆ 19 ژمارە، یان 16 ژمارە بە بۆشایی یان -)
    return bool(re.search(r'\d{13,19}|\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}', text))

def clean_text(text):
    """ستێرەکان و هێما زیادەکان لادەبات (تەنها بۆ کاپشنی میدیا)"""
    if not text:
        return ""
    text = text.replace("*", "")
    text = re.sub(r"(\d+)`", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    try:
        original_text = msg.text or ""
        
        # ئەم هێڵە زیادکراوە: ئەگەر کارتی تێدا نەبوو، دەستبەجێ بگەڕێوە و هیچ نەنێرە
        if not contains_card(original_text):
            return

        media = msg.media

        if media:
            file_path = await client.download_media(media)
            if file_path:
                caption = clean_text(original_text)
                await client.send_file(
                    TARGET_CHANNEL,
                    file_path,
                    caption=caption,
                )
                os.remove(file_path)
                print("✅ پەیامی میدیا + کاپشنی پاڵێوراو نێردرا.")
            else:
                if original_text.strip():
                    await client.send_message(TARGET_CHANNEL, original_text, formatting_entities=msg.entities)
                    print("✅ تەنها تەکست (بە فۆرمات) نێردرا.")
        else:
            if original_text.strip():
                await client.send_message(TARGET_CHANNEL, original_text, formatting_entities=msg.entities)
                print("✅ پەیامی تەکستی (ڕەسەن) نێردرا.")
    except Exception as e:
        print(f"❌ هەڵە: {e}")

async def main():
    await client.start()
    print("🚀 بۆت کاردەکات! تەنها پەیامەکانی تێدایە کارت دەنێردرێن.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
