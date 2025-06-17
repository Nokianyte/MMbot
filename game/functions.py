import asyncio
from random import randint

from bot.client import discord, client
from game.data.avatar import AVATAR_DICT
from game.data.items import ITEMS_DICT
from game.data.players import player_dict, PlayerBuilder, Action, Condition, add_player, set_player
from game.data.map import board, generate_board, spawn_players, set_board
from game.data.values import LOBBY_CHANNEL_ID
from utils.helpers import message, load_profile


async def start_game(ctx, pace):

    lobby_channel = client.get_channel(LOBBY_CHANNEL_ID)

    for member in lobby_channel.members:

        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = False

        await lobby_channel.set_permissions(member, overwrite = overwrite)

        new_channel = await ctx.guild.create_text_channel('🎮', overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        })

        avatar = load_profile(member.id)['avatar']

        add_player({member.id: PlayerBuilder().with_name(member.display_name).with_avatar(AVATAR_DICT[avatar['face']][avatar['skin']][avatar['hair']]).with_channel(new_channel.id).build()})

    generate_board()

    await spawn_players(ctx, player_dict)

    client.loop.create_task(start_clock(pace))

async def start_clock(pace):
    while True:
        for user_id in player_dict.keys(): await tick(user_id)
        await asyncio.sleep(pace)


async def tick(user_id): #данная функция запускается тактовым генератором для каждого объекта player. она проверяет ряд значений полей объекта, изменяет их. выглядит неэффективно, определённо требует оптимизации

    player = player_dict[user_id]

    if player.stats['Warmth']>=50 and player.stats['Warmth']+player.modifiers['Warmth']<=50: pass#await message()
    if player.stats['Hunger']>=50 and player.stats['Hunger']+player.modifiers['Hunger']<=50: pass#await message()
    if player.stats['Health']>=50 and player.stats['Health']+player.modifiers['Health']<=50: pass#await message()
    if player.stats['Sanity']>=50 and player.stats['Sanity']+player.modifiers['Sanity']<=50: pass#await message()
    if player.stats['Stamina']>=50 and player.stats['Stamina']+player.modifiers['Stamina']<=50: pass#await message()

    '''
    if player.statStamina<50:
        if randint(0,100)<=((50-player.statStamina)/50)*10: player.sleep()
    if player.statSanity<50:
        if randint(0,100)<=((50-player.statSanity)/50)*10: player.breakdown()
    '''

    player.add_ticks(-1)
    player.add_stats('Warmth', player.modifiers['Warmth'])
    player.add_stats('Hunger', player.modifiers['Hunger'])
    player.add_stats('Health', player.modifiers['Health'])
    player.add_stats('Sanity', player.modifiers['Sanity'])
    player.add_stats('Stamina', player.modifiers['Stamina'])
    if player.cooldown>-1: player.add_cooldown(-1)

    #player.modStrength = player.statWarmth*player.statHunger*player.statHealth*player.statStamina*(1-player.statWeight/20)*(0.02**4) #VARIABLE

    player.set_modifiers('Warmth', 0) #later
    player.set_modifiers('Stamina', 0)
    player.set_modifiers('Hunger', -0.14)
    player.set_modifiers('Health', (-(Condition.BLEEDING in player.conditions)-(Condition.POISONED in player.conditions)-(Condition.BURNING in player.conditions)*2+((player.stats['Warmth']-50)-abs(player.stats['Warmth']-50)*0.5)*0.01+((player.stats['Hunger']-50)-abs(player.stats['Hunger']-50)*0.5)*0.01)*0.2) #VARIABLE
    player.set_modifiers('Sanity', ((player.stats['Warmth']-50)+(player.stats['Hunger']-50)+(player.stats['Health']-50)+(player.stats['Stamina']-50)-100)*0.01*0.14) #VARIABLE
 #   self.modStamina=-(self.statWeight/self.maxWeight)*0.07+(-(self.action=='walking')-(self.action=='running')*3-(self.action=='hunting')-(self.action=='hiding'))*0.5*0.07-0.07 #VARIABLE

    if player.stats['Warmth']<0: player.set_stats('Warmth', 0)
    if player.stats['Hunger']<0: player.set_stats('Hunger', 0)
    if player.stats['Health']<=0: pass
    if player.stats['Sanity']<=0: pass
    if player.stats['Stamina']<=0: pass

    match player.action:
        case Action.LOOTING: #предметы добавляются в инвнтарь к игроку по истечению кулдауна
            player.add_modifiers('Stamina', -0.1)
            if player.ticks==0:
                item = board[player.xCoord][player.yCoord].loot.pop(randint(0,len(board[player.xCoord][player.yCoord].loot)-1))
                board[player.xCoord][player.yCoord].append_loot(None)
                if item != None:
                    if item in player.inventory: player.set_item(item, player.inventory[item] + 1)
                    else: player.add_item(item, 1)
                    await message(user_id, f"## + {ITEMS_DICT[item].emoji}") 
                player.set_ticks(2)    #int((16-player.modifiers['Strength'])+5) #VARIABLE
        case Action.RESTING:
            player.set_modifiers('Stamina', 0.2)
        case Action.SLEEPING:
            player.set_modifiers('Stamina', 0.8)
        case Action.BREAKDOWN:
            pass
        case Action.KNOCKEDOUT:
            player.set_modifiers('Stamina', 0.07)  

    if player.stats['Warmth']>100: player.set_stats('Warmth', 100)
    if player.stats['Hunger']>100: player.set_stats('Hunger', 100)
    if player.stats['Health']>100: player.set_stats('Health', 100)
    if player.stats['Sanity']>100: player.set_stats('Sanity', 100)
    if player.stats['Stamina']>100: player.set_stats('Stamina', 100)
