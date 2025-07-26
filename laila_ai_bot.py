from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from gtts import gTTS
import os
import random

# --- Bot Credentials ---
import os  # Add this at the top of your file if not already present

api_id = 25427040
api_hash = "1f0376de02e45ada535faf115efc0a57"
bot_token = "8070478670:AAFjyTy5-xbQLbCF-y5LvuCvOUNs-aN35sM"
openrouter_api_key = ""  # Leave blank to use OpenRouter default free models

app = Client("laila_ai_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# --- Flirty text replies lists ---
flirty_starts = [
    "Hey cutie 😘 I'm Laila AI — ready to whisper secrets!",
    "Hello handsome 😍... Laila AI at your service!",
    "Hi dear! Laila AI here. Ask me anything naughty or nice 😉"
]
flirty_replies = [
    "Hmm, that sounds interesting... you're full of surprises! 💕",
    "Aww, you're making me blush... Tell me more 😳",
    "You're too sweet! I could talk to you all day 🥰",
    "You always know how to make me smile 😌"
]

def get_ai_reply(prompt: str) -> str:
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {openrouter_api_key}"} if openrouter_api_key else {}
        data = {"model": "deepseek/deepseek-r1:free", "messages":[{"role":"user","content":prompt}]}
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return random.choice(flirty_replies)

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text(random.choice(flirty_starts))

@app.on_message(filters.command("help"))
def help_command(client, message: Message):
    message.reply_text(
        "📜 *Laila AI Commands:*\n"
        "/start - Start talking to me 😉\n"
        "/help - Show this help\n"
        "/about - Know about me\n"
        "/voice - Get a voice reply\n"
        "/pic - I'll send you a flirty image!"
    )

@app.on_message(filters.command("about"))
def about(client, message: Message):
    message.reply_text("I'm *Laila AI*, built to charm you with words, pics & voice. Always here to listen 😘")

@app.on_message(filters.command("pic"))
def send_picture(client, message: Message):
    images = ["flirty1.jpg","flirty2.jpg","flirty3.jpg"]
    img = random.choice(images)
    client.send_photo(message.chat.id, photo=img, caption="Here’s something cute for you 😍")

@app.on_message(filters.command("voice"))
def voice_reply(client, message: Message):
    txt = get_ai_reply(message.reply_to_message.text if message.reply_to_message else "Hey!")
    tts = gTTS(txt, lang="en")
    file = "voice.mp3"
    tts.save(file)
    client.send_audio(message.chat.id, audio=file, voice=True)
    os.remove(file)

@app.on_message(filters.text & ~filters.command(["start", "help", "about", "pic", "voice"]))
def chat(client, message: Message):
    ai = get_ai_reply(message.text)
    flirty = random.choice(flirty_replies)
    message.reply_text(f"💬 You said: *{message.text}*\n{ai}\n\n{flirty}")

@app.on_message(filters.command("ban"))
def ban_user(client, message: Message):
    message.reply_text("🚫 Sorry babe, ban feature isn’t ready yet!")

@app.on_message(filters.command("unban"))
def unban_user(client, message: Message):
    message.reply_text("✅ Back in action! Laila AI is here 😉")

app.run()