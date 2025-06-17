from bot.client import discord, client, tree

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1370677493685817344))
    print("Ready!")