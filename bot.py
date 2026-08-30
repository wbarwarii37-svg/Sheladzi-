import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== ڕێکخستنەکان ==================
API_ID = 33790522
API_HASH = "00e4131295f55452e143c06099c1ddae"

SESSION_STRING = "1ApWapzMBu4Y3MqRS0V1rAt4LTWWDNc1nQ-7RjQe0_9TjhYnuH37imYewBUlKyAQKjhYCLmqxGeDLCuyxs74MByvvM_ZI4YO0CN_9pu3JUFDjf2mXWkNVAdVN6kkTWzmTbXLiLzXTxaMIH65YUSECfTX-m-RKa6RaVC6LdwtMq-9aWV8hid6Fzgz5qxHnqUH7QLjn7ZshfpVufhut_pBbOQQBSLPiMfp00bFDAe1dell8pie3R4SDabuVGaAXCPZC2gt9peBdR4AgriM6Z0Z02KouMh8NgZOmw5Nt6fciEvYFgpGTOx_kmMh-yk1NCFSd3rMz2xY-9HTFu9REcz40H3ssa51IJ50="

# 🔴 گۆڕدرا بۆ ناوە نوێکان
SOURCE_CHANNEL = "@kroabscrap"    # سەرچاوە
TARGET_CHANNEL = "@Cc428Kurd"     # ئامانج
# ====================================================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def extract_card_info(text):
    """
    کارت، بانک و وڵات لە دەقەکەدا دەدۆزێتەوە.
    گەڕاندنەوەی لیستێک لە هەموو کارتەکان.
    """
    results = []
    blocks = re.split(r'\n\s*\n', text)
    
    for block in blocks:
        cc_match = re.search(r'(\b\d{15,16}\b)', block)
        if not cc_match:
            continue
        
        cc_num = cc_match.group(1)
        
        bank_match = re.search(r'Bank\s*[:=]\s*(.+?)(?:\n|$)', block, re.IGNORECASE)
        bank = bank_match.group(1).strip() if bank_match else "N/A"
        
        country_match = re.search(r'Country\s*[:=]\s*(.+?)(?:\n|$)', block, re.IGNORECASE)
        country = country_match.group(1).strip() if country_match else "N/A"
        
        results.append({
            "cc": cc_num,
            "bank": bank,
            "country": country
        })
    
    return results

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        text = event.message.text or ""
        cards = extract_card_info(text)
        
        if not cards:
            print("⏭️ هیچ کارتێک نەدۆزرایەوە، پەیامەکە فڕێدرا.")
            return
        
        output = []
        for card in cards:
            output.append(f"💳 {card['cc']}")
            output.append(f"🏦 {card['bank']}")
            output.append(f"🌍 {card['country']}")
            output.append("")
        
        final_text = "\n".join(output).strip()
        
        if final_text:
            await client.send_message(TARGET_CHANNEL, final_text)
            print(f"✅ {len(cards)} کارت نێردران بۆ @Cc428Kurd.")
    
    except Exception as e:
        print(f"❌ هەڵە: {e}")

async def main():
    await client.start()
    print("🚀 سکرێپتەکە کاردەکات...")
    print(f"📡 سەرچاوە: {SOURCE_CHANNEL}")
    print(f"🎯 ئامانج: {TARGET_CHANNEL}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
