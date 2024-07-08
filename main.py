# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

class Player:
    def __init__(self, constRole, constTraits, constStrength, obj_status, location, inventory, turns_left, stamina, statWarmth, statHunger, statHealth, statStamina, condCombat, condKnockedOut, condAsleep, condBurning, condBleeding, condPoison, condHidden, condFakingDead, condFakingKnockedOut):
        self.constRole = constRole
        self.constTraits = constTraits
        self.constStrength = constStrength

        self.obj_status = obj_status
        self.location = location
        self.inventory = inventory
        self.turns_left = turns_left
        self.stamina = stamina

        self.statWarmth = statWarmth
        self.statHunger = statHunger
        self.statHealth = statHealth
        self.statStamina = statStamina

        self.condCombat = condCombat
        self.condKnockedOut = condKnockedOut
        self.condAsleep = condAsleep
        self.condBurning = condBurning
        self.condBleeding = condBleeding
        self.condPoison = condPoison
        self.condHidden = condHidden
        self.condFakingDead = condFakingDead
        self.condFakingKnockedOut = condFakingKnockedOut

    def move():
    def loot():
    def give():
    def search_player():
    def craft():
    def use():
    def attack():
    def hide():
    def fakeDeath():
    def fakeKnockOut():
    def forfeit():

class Room:
    def __init__(self, loot, near_rooms, displayed_loot, players, burning):
        self.loot = loot
        self.near_rooms = near_rooms
        self.displayed_loot = displayed_loot
        self.players = players
        self.burning = burning

bot.run(TOKEN)