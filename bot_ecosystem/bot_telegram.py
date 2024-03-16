from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from bot_ecosystem.ai_system import *

# Load environment variables
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
model_path = os.getenv('MODEL_PATH')

# Create the client and connect
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    '''send message when the command /start is issued.'''
    await event.reply('Halo, saya alpher fungsi saya untuk')

@bot.on(events.NewMessage(pattern='/sentimen'))
async def echo(event):
    '''send message when the command /sentimen is issued.'''
    data = event.text.split()
    data.pop(0)
    data = ' '.join(data)
    respone = predict_sentiment('model',data)
    respone = f'sentimennya adalah {respone}'
    await event.respond(respone)
@bot.on(events.NewMessage(pattern='/echo'))
async def echo(event):
    '''send message when the command /echo is issued.'''
    print(event.date, event.peer_id)
    await event.respond(event.text)
def run():
    '''start the bot'''
    print("alpher connected")
    bot.run_until_disconnected()