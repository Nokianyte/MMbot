# client.py
import os

import json
from random import randint

import discord
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import tasks, commands

from player.players import *
from map.map import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1370677493685817344))
    print("Ready!")

class Timer(commands.Cog): #генератор тиков
    def __init__(self):
        self.trigger.start()

    def stop(self):
        self.trigger.cancel()

    @tasks.loop(seconds=10.0) # триггерится каждые 2 секунды
    async def trigger(self):
        for player in player_dict: tick(player)

# СПИСОК КОМАНД
'''
@client.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@tree.command(
    name="join",
    description="must be in a voice channel",
    guild=discord.Object(id=1370677493685817344)
)
async def join(ctx):
    member = ctx.user
    guild = ctx.guild
    
    channel_name = member.name

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True)
    }

    new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
    
    add_player(user=member)
    await ctx.response.send_message('_',ephemeral=True)

@client.command()
async def clone(ctx, arg):
    channel = client.get_channel(1262061733606981714)
    await channel.clone(name=arg)
'''
@tree.command(
    name="quit",
    description="quits the game",
    guild=discord.Object(id=1370677493685817344)
)
async def leave(ctx):

    global player_dict
    global board

    user = ctx.user.id
    player = player_dict[user]
    tile = board[player.xCoord][player.yCoord]

    await delete_channel(player.text_channel_id)
    player_dict.pop(user)
    tile.players.remove(user)

    await move_to_vc(ctx, int(user), None)

    if len(tile.players) == 0:
        tile.channel = await delete_channel(tile.channel)

    with open('ingame_values.json') as f:

        ing_values = json.load(f)

        lobby_channel = client.get_channel(ing_values['lobby_channel_id'])

        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = True

        await lobby_channel.set_permissions(ctx.user, overwrite = overwrite)


'''
@client.command()
async def stat(ctx, user: discord.Member = None):
    if user == None:
        print(player_dict[find_player(ctx.author.nick)].stats)
'''

@tree.command(
    name="start_game",
    description="must be in a voice channel",
    guild=discord.Object(id=1370677493685817344)
)
async def start(ctx):

    global board

    ing_values = load_values()

    lobby_channel = client.get_channel(ing_values['lobby_channel_id'])

    for member in lobby_channel.members:

        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = False

        await lobby_channel.set_permissions(member, overwrite = overwrite)

        new_channel = await ctx.guild.create_text_channel('🎮', overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        })

        add_player(member.id, member.nick, new_channel.id)

    board = generate_map()

    await spawn_players(ctx)

    #Timer()

    await ctx.response.send_message('Игра началась!',ephemeral=True)

@tree.command(
    name="move",
    description="between tiles",
    guild=discord.Object(id=1370677493685817344)
)
@app_commands.choices(choices=[
    app_commands.Choice(name="north", value=0),
    app_commands.Choice(name="south", value=1),
    app_commands.Choice(name="east", value=2),
    app_commands.Choice(name="west", value=3)
])
async def move(ctx, choices: app_commands.Choice[int]):

    global player_dict
    global board

    player = player_dict[ctx.user.id]

    old_tile = board[player.xCoord][player.yCoord]

    match choices.value:
        case 0:
            if player.yCoord < len(board):
                new_tile = board[player.xCoord][player.yCoord + 1]
                player.yCoord += 1
            else: 
                await ctx.response.send_message('At border',ephemeral=True)
                return
        case 1:
            if player.yCoord > 0:
                new_tile = board[player.xCoord][player.yCoord - 1]
                player.yCoord -= 1
            else: 
                await ctx.response.send_message('At border',ephemeral=True)
                return
        case 2:
            if player.xCoord < len(board):
                new_tile = board[player.xCoord + 1][player.yCoord]
                player.xCoord += 1
            else: 
                await ctx.response.send_message('At border',ephemeral=True)
                return
        case 3:
            if player.xCoord > 0:
                new_tile = board[player.xCoord - 1][player.yCoord]
                player.xCoord -= 1
            else: 
                await ctx.response.send_message('At border',ephemeral=True)
                return

    old_tile.players.remove(ctx.user.id)
    new_tile.players.append(ctx.user.id)

    if len(new_tile.players) == 1:
        new_tile.channel = await create_vc(ctx, new_tile.terrain)

    await move_to_vc(ctx, ctx.user.id, new_tile.channel)

    if len(old_tile.players) == 0:
        old_tile.channel = await delete_channel(old_tile.channel)

    await ctx.response.send_message(f"Moved to {new_tile.terrain}",ephemeral=True)
            
##

async def create_vc(ctx, channel_name):
    guild = ctx.guild

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }

    new_channel = await guild.create_voice_channel(channel_name, overwrites=overwrites)
    return new_channel.id

async def delete_channel(id):
    channel = client.get_channel(id)
    await channel.delete()
    return None

async def move_to_vc(ctx, user_id, channel_id):
    channel = client.get_channel(channel_id)
    user = await ctx.guild.fetch_member(user_id)
    await user.move_to(channel)

def load_values():
    with open('ingame_values.json') as f:
        return json.load(f)

#внутреигровые функции

async def spawn_players(ctx):

    global player_dict
    global board

    values = load_values()

    xSpawn = values['spawn_point']['xCoord']
    ySpawn = values['spawn_point']['yCoord']

    spawn_point = board[xSpawn][ySpawn]

    spawn_point.channel = await create_vc(ctx, spawn_point.terrain)

    for user_id, player in player_dict.items():
        spawn_point.players.append(user_id)
        player.xCoord, player.yCoord = xSpawn, ySpawn
        await move_to_vc(ctx, user_id, spawn_point.channel)

async def tick(self): #данная функция запускается тактовым генератором для каждого объекта player. она проверяет ряд значений полей объекта, изменяет их. выглядит неэффективно, определённо требует оптимизации

    if self.statWarmth>100: self.statWarmth=100
    if self.statHunger>100: self.statHunger=100
    if self.statSanity>100: self.statSanity=100
    if self.statStamina>100: self.statStamina=100

    if self.statWarmth>=50 and self.statWarmth+self.modWarmth<=50: pass#await message()
    if self.statHunger>=50 and self.statHunger+self.modHunger<=50: pass#await message()
    if self.statHealth>=50 and self.statHealth+self.modHealth<=50: pass#await message()
    if self.statSanity>=50 and self.statSanity+self.modSanity<=50: pass#await message()
    if self.statStamina>=50 and self.statStamina+self.modStamina<=50: pass#await message()

    if self.statStamina<50:
        if randint(0,100)<=((50-self.statStamina)/50)*10: self.sleep()
    if self.statSanity<50:
        if randint(0,100)<=((50-self.statSanity)/50)*10: self.breakdown()

    self.ticks-=1
    self.statWarmth+=self.modWarmth
    self.statHunger+=self.modHunger
    self.statHealth+=self.modHealth
    self.statSanity+=self.modSanity
    self.statStamina+=self.modStamina
    if self.cooldown>-1: self.cooldown-=1

    self.modStrength = self.statWarmth*self.statHunger*self.statHealth*self.statStamina*(1-self.statWeight/20)*(0.02**4) #VARIABLE

    self.modWarmth=0 #later
    self.modHunger=-0.07
    self.modHealth=(-(Condition.BLEEDING in self.condition)-(Condition.POISONED in self.condition)-(Condition.BURNING in self.condition)*2+((self.statWarmth-50)-abs(self.statWarmth-50)*0.5)*0.01+((self.statHunger-50)-abs(self.statHunger-50)*0.5)*0.01)*0.2 #VARIABLE
    self.modSanity=((self.statWarmth-50)+(self.statHunger-50)+(self.statHealth-50)+(self.statStamina-50)-100)*0.01*0.07 #VARIABLE
 #   self.modStamina=-(self.statWeight/self.maxWeight)*0.07+(-(self.action=='walking')-(self.action=='running')*3-(self.action=='hunting')-(self.action=='hiding'))*0.5*0.07-0.07 #VARIABLE

    if self.statWarmth<0: self.statWarmth=0
    if self.statHunger<0: self.statHunger=0
    if self.statHealth<=0: self.die()
    if self.statSanity<=0: self.die()
    if self.statStamina<=0: self.die()

    match self.action:
        case Action.LOOTING: #предметы добавляются в инвнтарь к игроку по истечению кулдауна
            if self.ticks==0:
                item = board[self.xCoord][self.yCoord].loot.pop(randint(0,len(board[self.xCoord][self.yCoord].loot)-1))
                board[self.xCoord][self.yCoord].loot.append(None)
                if item != None:
                    self.inventory.append(item)
#                    message() 
                self.ticks=int((16-self.statStrength)+5) #VARIABLE
        case Action.RESTING:
            self.modStamina=0.1
        case Action.SLEEPING:
            if self.statStamina>=100:
                self.wake_up()
            else:
                self.modStamina=0.4
        case Action.BREAKDOWN:
            pass
        case Action.KNOCKEDOUT:
            self.modStamina=0.07
            if self.cooldown=='0':
                self.wake_up()            

client.run(TOKEN)

#channel = discord.utils.get(ctx.guild.channels, name=given_name)
#channel_id = channel.id

#1263066199961632778