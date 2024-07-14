# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from random import randint

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

@bot.command()
async def join(ctx, user: discord.Member = None):
    add_player(user)
    print(player_list)
    guild = ctx.message.guild
    await guild.create_text_channel(f'личный канал {user}')

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

class Player:
    def __init__(self, user, name, constTraits, constStrength, xCoord, yCoord, inventory, action, statWarmth, statHunger, statHealth, statStamina, statWeight, condCombat, condKnockedOut, condAsleep, condBurning, condBleeding, condPoison, condHidden, condFakingDead, condFakingKnockedOut):
        self.user = user
        self.name = name
        self.constTraits = constTraits
        self.constStrength = constStrength

        self.xCoord = xCoord
        self.yCoord = yCoord
        self.inventory = inventory
        self.action = action

        self.statWarmth = statWarmth
        self.statHunger = statHunger
        self.statHealth = statHealth
        self.statStamina = statStamina
        self.statWeight = statWeight

        self.condCombat = condCombat
        self.condKnockedOut = condKnockedOut
        self.condAsleep = condAsleep
        self.condBurning = condBurning
        self.condBleeding = condBleeding
        self.condPoison = condPoison
        self.condHidden = condHidden
        self.condFakingDead = condFakingDead
        self.condFakingKnockedOut = condFakingKnockedOut

    def move(direction):
        pass
    def loot():
        pass
    def give(player, object):
        pass
    def search_player(player):
        pass
    def craft(object):
        pass
    def use(object, action):
        pass
    def hunt():
        pass
    def attack(player):
        pass
    def hide():
        pass
    def rest():
        pass
    def sleep(duration):
        pass
    def fakeDeath():
        pass
    def fakeKnockOut():
        pass
    def forfeit():
        pass

class Room:
    def __init__(self, channel, type, xCoord, yCoord, loot, content, entities, burning):
        self.channel = channel
        self.type = type
        self.yCoord = yCoord
        self.xCoord = xCoord
        self.loot = loot
        self.content = content
        self.entities = entities
        self.burning = burning

## ITEM ##

class Item:
    def __init__(self, name, id, type, char, weight):
        self.name=name
        self.id=id
        self.type=type
        self.char=char
        self.weight=weight

item_list = [

    Item('Консервированная тушёнка',0,'food',20,0.3),
    Item('Консервированные овощи',1,'food',10,0.3),
    Item('Сухпаёк',2,'food',10,0.1),
    Item('Мясо животного',3,'food',10,0.3),
    Item('Жаренное мясо животного',4,'food',30,0.3),
    Item('Рыба',5,'food',10,0.2),
    Item('Жаренная рыба',6,'food',30,0.2),
    Item('Человеческое мясо',7,'food',10,0.3),
    Item('Жаренное человеческое мясо',8,'food',30,0.3),

    Item('Антибиотики',9,'consumable',None,0.1),
    Item('Бинты',10,'consumable',None,0.1),
    Item('Алкоголь',11,'consumable',None,0.3),

    Item('Маленький рюкзак',12,'storage',5,0.3),
    Item('Походный рюкзак',13,'storage',15,1),

    Item('Тёплая одежда',14,'clothes',20,1),
    Item('Камуфляж',15,'clothes',5,0.5),

    Item('Ледоруб',16,'weapon',None,0.5),
    Item('Складной нож',17,'weapon',None,0.2),
    Item('Топор',18,'weapon',None,1),
    Item('Деревянный кол',19,'weapon',None,0.5),

    Item('Пистолет',20,'gun',None,0.5),
    Item('Ружье',21,'gun',None,1),
    Item('Винтовка',22,'gun',None,1),
    Item('Самодельный лук',23,'gun',None,0.5),

    Item('Пистолетный патрон',24,'ammo',None,0.1),
    Item('Ружейный патрон',25,'ammo',None,0.1),
    Item('Винтовочный патрон',26,'ammo',None,0.1),
    Item('Самодельная стрела',27,'ammo',None,0.2),

    Item('Сеть',28,'trap',None,0.2),
    Item('Капкан',29,'trap',None,1),

    Item('Древисина',30,'resource',None,0.3),
    Item('Камень',31,'resource',None,0.3),
    Item('Шкура',32,'resource',None,0.3),
    Item('Ткань',33,'resource',None,0.1),

    Item('Швейные принадлежности',34,'other',None,0.1),
    Item('Компас',35,'other',None,0.2),
    Item('Рация',36,'other',None,0.2),
    Item('Батарейка',37,'other',None,0.1),
    Item('Фонарик',38,'other',None,0.2),
    Item('Зажигалка',39,'other',None,0.1),
    Item('Факел',40,'other',None,0.2),
    Item('Коктейль Молотова',41,'other',None,0.3),
    Item('Стеклянная бутылка',42,'other',None,0.2),
    Item('Справочник по выживанию',43,'other',None,0.2),
    Item('Книга Обрядов',44,'other',None,0.3),
    Item('Бензин',45,'other',None,0.5)

]

##

player_list = []

def create_lobby(mode):
    ## adds everyone sitting in a set voice chennel to player list
    pass

def create_channel(name):
    channel = bot.get_channel(1262061733606981714)
    channel.clone(name=name)
    channel = discord.utils.get(ctx.guild.channels, name=name)
    return channel.id

def delete_channel(id):
    channel = bot.get_channel(id)
    channel.delete()
    return None

def add_player(user):
    player_list.append(Player(user=user, name=user.nick, constTraits=[], xCoord=0, yCoord=0, inventory=[], action=None, statWarmth=100, statHunger=100, statHealth=100, statStamina=100, statWeight = 5, condCombat=False, condKnockedOut=False, condAsleep=False, condBurning=False, condBleeding=False, condPoison=False, condHidden=False, condFakingDead=False, condFakingKnockedOut=False))

def remove_player(user):
    player_list.pop(find_player(user)) 

def find_player(user):
    for i in range(len(player_list)):
        if player_list[i].user==user:
            return i

bot.run(TOKEN)

#channel = discord.utils.get(ctx.guild.channels, name=given_name)
#channel_id = channel.id