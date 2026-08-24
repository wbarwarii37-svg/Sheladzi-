import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ========== ڕێکخستنەکان ==========
api_id = 33774652
api_hash = "c438941d8f43a0ff59fcc4b3f3c2fb42"
session = "1AZWarzgBuxQ0-aioaIlPwwMcXEHKxWIoidYTLWn0X1pGKeQYqQkd8QwSORpRU821YgSC3svKav8TeQwxtfpK1Eolxt_ADEg8tVnWV1ApziV3QOoc5ZTJWhD4oo8YsDfnCPy1hF8OO-GI9IOH0YggSGykM8QamZR3D8WEZVg4KiBIIxeuOAS9u38QWFfUNJTlJCgGL9rSWS3SJ2dZutG2zdFhYM0gRRi8jXIejA8NlkH5gASq9SJHSMcdkeF9a6e3dqyqZGKDRwXQIc5ZVT4ejdIgdhHm1GEE76ecw2hM6U8Ojypz36iR_1Tf_0aQIVcS9Yy3vP2RFWqZsQRYnYQq8_rseVUjvd0="

SOURCE_CHANNEL = "@SlimeChkGroup"
TARGET_CHANNEL = "@Duhok65"

# ========== تەنها پەیامەکانی ئەم ناوە ==========
ALLOWED_DEV = "@RimuruCHK"
# =============================================

def format_card_data(text):
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

    if msg.media:
        return
    
    url_pattern = r'https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+'
    if re.search(url_pattern, original_text):
        return

    if "Bank: N/A" in original_text or "Country: N/A" in original_text or "Type: N/A" in original_text:
        return

    # ========== تەنها ئەم کەسە ==========
    if ALLOWED_DEV not in original_text:
        return
    # ===================================

    original_text = original_text.replace("@About_Warnix", "@warven_24")
    original_text = original_text.replace("@Warrixx", "@warven_24")
    original_text = original_text.replace("@Warnisx", "@warven_24")
    original_text = original_text.replace("@About_Warnisx", "@warven_24")

    new_text = format_card_data(original_text)
    await client.send_message(TARGET_CHANNEL, new_text)

print(f"Bot is running... (تەنها پەیامەکانی {ALLOWED_DEV} دەنێردرێت بۆ @Duhok65)")
client.start()
client.run_until_disconnected()
