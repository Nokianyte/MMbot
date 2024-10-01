import discord
import asyncio

client = discord.Client()

day=0

async def time_cycle():
    while True:
        await asyncio.sleep(120)
        time='утро'
        await asyncio.sleep(120)
        time='день'
        await asyncio.sleep(120)
        time='вечер'
        await asyncio.sleep(120)
        time='ночь'
        day_number+=1
