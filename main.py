# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands

from players import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=1.0)
    async def printer(self):
        print(self.index)
        self.index += 1

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def join(ctx):
    member = ctx.author
    guild = ctx.guild
    channel_name = member.name

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True)
    }

    new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

    add_player(user=member, channel=new_channel.id)
    print(player_list)

@bot.command()
async def clone(ctx, arg):
    channel = bot.get_channel(1262061733606981714)
    await channel.clone(name=arg)

@bot.command()
async def leave(ctx, user: discord.Member = None):
    remove_player(user)
    print(player_list)

@bot.command()
async def stat(ctx, user: discord.Member = None):
    print(player_list[find_player(user)].statHealth)

##

def create_lobby(mode):
    ## adds everyone sitting in a set voice chennel to player list
    pass

def create_vc(name):
    channel = bot.get_channel(1262061733606981714)
    channel.clone(name=name)
    new_channel = discord.utils.get(ctx.guild.channels, name=name)
    return new_channel.id

def delete_channel(id):
    channel = bot.get_channel(id)
    channel.delete()
    return None

def move_to_vc(user, id):
    channel = bot.get_channel(id)
    user.move_to(channel)

bot.run(TOKEN)

#channel = discord.utils.get(ctx.guild.channels, name=given_name)
#channel_id = channel.id

#1263066199961632778