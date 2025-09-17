from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

from bot_ecosystem.ai_system import predict_sentiment

# Load environment variables
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# Create the client and connect
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """send message when the command /start is issued."""
    await event.reply('Halo, saya alpher fungsi saya untuk')

@bot.on(events.NewMessage(pattern='/sentimen'))
async def sentimen(event):
    """send message when the command /sentimen is issued."""
    data = event.text.split()
    data.pop(0)
    data = ' '.join(data)
    response = predict_sentiment(data)
    response = f'sentimennya adalah {response}'
    await event.respond(response)

@bot.on(events.NewMessage(pattern='/echo'))
async def echo(event):
    """send message when the command /echo is issued."""
    print(event.date, event.peer_id)
    await event.respond(event.text)

def run():
    """start the bot"""
    print("alpher connected")
    bot.run_until_disconnected()
