import asyncio
import re
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== ڕێکخستنەکان ==================
API_ID = 33774652
API_HASH = "c438941d8f43a0ff59fcc4b3f3c2fb42"
SESSION_STRING = "1AZWarzgBuyCyj8c2ma6tF7RdpXUH89YLsev7Vpm5tk7WFP_s8k5eqa517QhiOqwbwDMrA9GWOz1nu0fFdsmNhYTfJSAN4lZrC2HusHff-ZcB3gQz6L9SuMZa-POX-rdtA7vZb35B1x8hLoDo18xK6jdvA7iEBGrFfQlA5RG3_65EkikA24ZMIQggek5eDkOBt6aIgpsZC5xSwlxstsMxSC2QiPoyqQSsts7vGQHlJQYvAs7_pCW42ZyF_E7UkBIg0rIEJ7odgs9Fi1_8A0mlOsIblU8H0tLIu3CaoI20XHXgz6shFxE7sCOh5Yc8QUGkVFBNkmY6BAz65XInIHi-fivB9LnvANc="

SOURCE_CHANNEL = "@AdvancedScraper"   # سەرچاوە (لە وێنەدا AdvancedScraper)
TARGET_CHANNEL = "@Cc428Card"         # ئامانج
# ====================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def extract_cc_info(text):
    """
    ژمارەی کارت، بانک و وڵات لە دەقەکەدا دەدۆزێتەوە.
    گەڕاندنەوەی لیستێک لە فەرهەنگ (هەر کارتێک و زانیارییەکانی).
    """
    results = []
    # پێشنیاری regex بۆ ژمارەی کارت (١٥ یان ١٦ ژمارە، دەکرێت بە | جیا بکرێتەوە)
    cc_pattern = r"(\b\d{15,16}\b)(?:\s*[|]\s*(\d{1,2})\s*[|]\s*(\d{1,2})\s*[|]\s*(\d{3,4})\b)?"
    # بەدواداچوون بۆ کارتەکان
    parts = re.split(r"\n\s*\n", text)  # جیاکردنەوەی بەشەکان بەپێی ڕیزی بەتاڵ
    for part in parts:
        # دۆزینەوەی ژمارەی کارت
        cc_match = re.search(cc_pattern, part)
        if not cc_match:
            continue
        cc_num = cc_match.group(1)
        # دۆزینەوەی بانک
        bank_match = re.search(r"Bank\s*:\s*(.+?)(?:\n|$)", part, re.IGNORECASE)
        bank = bank_match.group(1).strip() if bank_match else "N/A"
        # دۆزینەوەی وڵات
        country_match = re.search(r"Country\s*:\s*(.+?)(?:\n|$)", part, re.IGNORECASE)
        country = country_match.group(1).strip() if country_match else "N/A"
        # دۆزینەوەی Gate (ئەگەر پێویست بێت، بەڵام وەک بانک و وڵات نادرێت)
        results.append({
            "cc": cc_num,
            "bank": bank,
            "country": country
        })
    return results

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    try:
        original_text = msg.text or ""
        # دەرهێنانی زانیارییەکان
        cards = extract_cc_info(original_text)
        if not cards:
            # ئەگەر هیچ کارتێک نەدۆزرایەوە، پەیامەکە فڕێبدە (نەینێرە)
            print("⏭️ هیچ کارتێک نەدۆزرایەوە، پەیامەکە فڕێدرا.")
            return
        
        # دروستکردنی پەیامی نوێ بە تەنیا کارت، بانک و وڵات
        output_lines = []
        for card in cards:
            output_lines.append(f"💳 {card['cc']}")
            output_lines.append(f"🏦 {card['bank']}")
            output_lines.append(f"🌍 {card['country']}")
            output_lines.append("")  # ڕیزی بەتاڵ بۆ جیاکردنەوە
        
        output_text = "\n".join(output_lines).strip()
        
        if output_text:
            await client.send_message(TARGET_CHANNEL, output_text)
            print(f"✅ پەیام نێردرا (تەنیا کارت+بانک+وڵات)")
    except Exception as e:
        print(f"❌ هەڵە: {e}")

async def main():
    await client.start()
    print("🚀 بۆت کاردەکات! تەنیا کارت، بانک و وڵات دەنێرێت.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
