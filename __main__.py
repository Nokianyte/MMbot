import os
from bot.events import on_ready
from bot.commands import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client.run(TOKEN)