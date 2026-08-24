import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ========== ڕێکخستنەکان ==========
api_id = 33774652
api_hash = "c438941d8f43a0ff59fcc4b3f3c2fb42"
session = "1ApWapzMBu7hz-BUMCTEjbC3t3zhPhDubVBihygXIVGzxds9frt9vjLcVD1Nv_8kDD7R6Rkm5vI39-CFIgyvE9jWG4jOUK9YAVaShnjVWU8nSDe9IVCHwS5euDRw8M1RCgH589y4c-mWolHC_Kn9p5DzrqwLZrItxMQCxxW-5i5JleM1Ju4KL-G_UejLh5hwtARciZlsstCfWWWHqQ9T26oC-RYzzK1rWlIrOTQCJOBAbRw8ajfXaDQBGHeIJxv8HWdJNbvAljzz-oUFIPzLHo8YPWyTkKHOIycpSrjHfV4WGDCadb0D2S67vxOssTLMlKx7nFT8NeVqyQj1j6ugdEv6f1Gg37lc="

SOURCE_CHANNEL = "@SlimeChkGroup"
TARGET_CHANNEL = "@Duhok65"
# ===================================

def format_card_data(text):
    # گەڕان بۆ کارت
    cc_match = re.search(r'(\d{15,16})\s*\|\s*(\d{2})\s*\|\s*(\d{2,4})\s*\|\s*(\d{3,4})', text)
    if cc_match:
        cc, month, year, cvv = cc_match.groups()
        bin_num = cc[:6]
    else:
        return text

    bank_match = re.search(r'Bank:\s*(.+)', text, re.IGNORECASE)
    country_match = re.search(r'Country:\s*(.+)', text, re.IGNORECASE)
    type_match = re.search(r'Type:\s*(.+)', text, re.IGNORECASE)

    bank = bank_match.group(1).strip() if bank_match else "N/A"
    country = country_match.group(1).strip() if country_match else "N/A"
    card_type = type_match.group(1).strip() if type_match else "N/A"

    formatted = f"""KURD Scrapper by @warven_24

CC: `{cc}|{month}|{year}|{cvv}`
BIN: `{bin_num}`
Bank: {bank}
Country: {country}
Type: {card_type}

Developed By @warven_24"""

    extra_match = re.search(r'(\d+\s+\d+:\d+\s+[AP]M)$', text)
    if extra_match:
        formatted += f"\n\n{extra_match.group(1)}"
    
    return formatted

client = TelegramClient(StringSession(session), api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    original_text = msg.text or ""

    # پشتگوێخستنی وێنە و لینک
    if msg.media:
        return
    
    url_pattern = r'https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+'
    if re.search(url_pattern, original_text):
        return

    # ========== فلتری N/A ==========
    # ئەگەر Bank, Country, Type هەریەکێکیان N/A بوو، پەیامەکە پشتگوێ بخرێت
    if "Bank: N/A" in original_text or "Country: N/A" in original_text or "Type: N/A" in original_text:
        return
    # ================================

    # گۆڕینی هەموو ناوە ناخوازراوەکان بۆ @warven_24
    original_text = original_text.replace("@About_Warnix", "@warven_24")
    original_text = original_text.replace("@Warrixx", "@warven_24")
    original_text = original_text.replace("@Warnisx", "@warven_24")
    original_text = original_text.replace("@About_Warnisx", "@warven_24")

    new_text = format_card_data(original_text)
    await client.send_message(TARGET_CHANNEL, new_text)

print("Bot is running... (پەیامەکانی N/A نەنێردرێت)")
client.start()
client.run_until_disconnected()
