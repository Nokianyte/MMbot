from bot.client import discord, client, tree
from game.data.values import GUILD_ID

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


    