import asyncio
from random import randint

from bot.client import discord, client
from game.data.avatar import AVATAR_DICT
from game.data.display import DisplayFactory, DISPLAY_CONFIG
from game.data.items import ITEMS_DICT
from game.data.players import player_dict, PlayerBuilder, Action, Condition, add_player, set_player
from game.data.map import board, generate_board, spawn_players, set_board
from game.data.values import LOBBY_CHANNEL_ID
from utils.helpers import message, load_profile

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')


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

        display_factory = DisplayFactory(ctx.guild, member)
        
        for config in DISPLAY_CONFIG.values():
            await display_factory.create_category_with_channels(
                config['title'],
                config['channels']
            )

        avatar = load_profile(member.id)['avatar']

        add_player({member.id: PlayerBuilder().with_name(member.display_name).with_avatar(AVATAR_DICT[avatar['face']][avatar['skin']][avatar['hair']]).with_channel(new_channel.id).with_display(display_factory.get_all_ids()).build()})

        await new_channel.send(embed=create_player_stats_embed(player_dict[member.id]))

        await asyncio.sleep(2)

    generate_board()

    await spawn_players(ctx, player_dict)

    for player in player_dict.keys(): await update_map(player)

    client.loop.create_task(clock(pace))

async def clock(pace):
    while True:
        for user_id in player_dict.keys(): 
            try: await tick(user_id)
            except Exception as e: print(f"Error in tick for {user_id}: {e}")
        await asyncio.sleep(pace)

def create_bar(value):
    value +=5

    if value//10 > 7: color = "🟩"
    elif value//10 > 5: color = "🟨"
    elif value//10 > 2: color = "🟧"
    else: color = "🟥"

    return color*int(value//10) + "⬛"*int(10-value//10)

async def update_stat_display(user_id, stat):
    pass
'''
    percentage = player_dict[user_id].stats[stat] + 5
    if percentage//10 > 7: color = "🟩"
    elif percentage//10 > 5: color = "🟨"
    elif percentage//10 > 2: color = "🟧"
    else: color = "🟥"

    channel = client.get_channel(player_dict[user_id].display['🩻']['channels'][index])
    await channel.edit(name=(channel.name[:1] + color*int(percentage//10) + "⬛"*int(10-percentage//10)))'''


async def update_map(user_id):
    player = player_dict[user_id]
    player.set_map(player.xCoord, player.yCoord, player.avatar[0])

    if player.yCoord < len(board)-1: player.set_map(player.xCoord, player.yCoord + 1, board[player.xCoord][player.yCoord + 1].emoji[0])
    if player.yCoord > 0: player.set_map(player.xCoord, player.yCoord - 1, board[player.xCoord][player.yCoord - 1].emoji[0])
    if player.xCoord < len(board)-1: player.set_map(player.xCoord + 1, player.yCoord, board[player.xCoord + 1][player.yCoord].emoji[0])
    if player.xCoord > 0: player.set_map(player.xCoord - 1, player.yCoord, board[player.xCoord - 1][player.yCoord].emoji[0])

    for column in range(len(player.map)):
        channel = client.get_channel(player_dict[user_id].display['🗺️']['channels'][column])
        name=''
        for row in range(len(player.map)):
            name += player.map[row][4 - column]
        await channel.edit(name=(name))


async def tick(user_id):
    player = player_dict[user_id]
    
    # Кэшируем старые значения для сравнения
    old_stats = {
        'Warmth': player.stats['Warmth'] // 10,
        'Hunger': player.stats['Hunger'] // 10, 
        'Health': player.stats['Health'] // 10,
        'Sanity': player.stats['Sanity'] // 10,
        'Stamina': player.stats['Stamina'] // 10
    }
    
    # Основная логика тика
    player.add_ticks(-1)
    
    # Применяем модификаторы
    stats_to_update = await apply_modifiers(player)
    
    # Обрабатываем действия
    await handle_player_action(user_id)

    # Проверяем границы значений
    clamp_stats(player)
    
    # Обновляем UI только для изменившихся статов
    await update_changed_stats(user_id, old_stats, player)

async def apply_modifiers(player):
    """Применяет модификаторы и возвращает какие статы изменились"""
    # Применяем изменения
    player.add_stats('Warmth', player.modifiers['Warmth'])
    player.add_stats('Hunger', player.modifiers['Hunger']) 
    player.add_stats('Health', player.modifiers['Health'])
    player.add_stats('Sanity', player.modifiers['Sanity'])
    player.add_stats('Stamina', player.modifiers['Stamina'])
    
    # Обновляем модификаторы (упрощенная версия)
    player.set_modifiers('Warmth', 0)
    player.set_modifiers('Stamina', 0)
    player.set_modifiers('Hunger', -0.14)
    
    # Вычисляем сложные модификаторы
    health_mod = calculate_health_modifier(player)
    sanity_mod = calculate_sanity_modifier(player)
    
    player.set_modifiers('Health', health_mod)
    player.set_modifiers('Sanity', sanity_mod)
    player.set_modifiers('Strength', 10)
    
    if player.cooldown > -1:
        player.add_cooldown(-1)

def calculate_health_modifier(player):
    """Вычисляет модификатор здоровья"""
    base_penalty = (
        -(Condition.BLEEDING in player.conditions) -
        (Condition.POISONED in player.conditions) - 
        (Condition.BURNING in player.conditions) * 2
    )
    
    warmth_effect = ((player.stats['Warmth'] - 50) - abs(player.stats['Warmth'] - 50) * 0.5) * 0.01
    hunger_effect = ((player.stats['Hunger'] - 50) - abs(player.stats['Hunger'] - 50) * 0.5) * 0.01
    
    return (base_penalty + warmth_effect + hunger_effect) * 0.2

def calculate_sanity_modifier(player):
    """Вычисляет модификатор рассудка"""
    stat_sum = (
        (player.stats['Warmth'] - 50) +
        (player.stats['Hunger'] - 50) + 
        (player.stats['Health'] - 50) +
        (player.stats['Stamina'] - 50) - 100
    )
    return stat_sum * 0.01 * 0.14

async def handle_player_action(user_id):
    """Обрабатывает действия игрока"""
    player = player_dict[user_id]
        
    match player.action:
        case Action.LOOTING:
            await handle_looting(user_id)
        case Action.RESTING:
            player.set_modifiers('Stamina', 0.2)
        case Action.SLEEPING:
            player.set_modifiers('Stamina', 20)
        case Action.BREAKDOWN:
            pass
        case Action.KNOCKEDOUT:
            player.set_modifiers('Stamina', 0.07)

async def handle_looting(user_id):
    """Обрабатывает лутание"""
    player = player_dict[user_id]
    player.add_modifiers('Stamina', -0.1)
    
    tile = board[player.xCoord][player.yCoord]
    if tile.loot:
        item = tile.loot.pop(randint(0, len(tile.loot) - 1))
        tile.append_loot(None)
        
        if item is not None:
            if item in player.inventory:
                player.set_item(item, player.inventory[item] + 1)
            else:
                player.add_item(item, 1)
            await message(user_id, f"## + {ITEMS_DICT[item].emoji}")
    
    player.set_ticks(2)

def clamp_stats(player):
    """Ограничивает значения статов"""
    for stat in ['Warmth', 'Hunger', 'Health', 'Sanity', 'Stamina']:
        if player.stats[stat] < 0:
            player.set_stats(stat, 0)
        elif player.stats[stat] > 100:
            player.set_stats(stat, 100)

async def update_changed_stats(user_id, old_stats, player):
    """Обновляет только изменившиеся статы с обработкой ошибок"""
    for stat in ['Warmth', 'Hunger', 'Health', 'Sanity', 'Stamina']:
        new_value = player.stats[stat] // 10
        if old_stats[stat] != new_value:
            await safe_update_stat_display(user_id, stat)

async def safe_update_stat_display(user_id, stat):
    try:
        player = player_dict.get(user_id)
        if not player:
            logger.warning(f"Player {user_id} not found")
            return
            
        channel = client.get_channel(player.text_channel_id)
        if not channel:
            logger.warning(f"Channel {player.text_channel_id} not found for {user_id}")
            return
            
        # Проверяем права бота в канале
        if not channel.permissions_for(channel.guild.me).send_messages:
            logger.warning(f"No send permissions in channel {channel.id}")
            return
            
        logger.info(f"Updating {stat} for {user_id} in channel {channel.id}")
        # update_stat_display(user_id, stat)
        
    except discord.HTTPException as e:
        logger.error(f"HTTP error updating {stat} for {user_id}: {e.status} - {e.code}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


def create_player_stats_embed(player):
    """Создает embed со статистикой игрока"""
    
    # Определяем цвет по состоянию здоровья
    health_color = (
        discord.Color.green() if player.stats['Health'] > 70 else
        discord.Color.orange() if player.stats['Health'] > 30 else  
        discord.Color.red()
    )
    
    embed = discord.Embed(
        title=f"📊 {player.name}'s Statistics",
        color=health_color,
        timestamp=discord.utils.utcnow()
    )
    
    #embed.set_thumbnail(url=player.avatar_url or "https://example.com/default-avatar.png")
    
    # Основные статы
    stat_icons = {'Warmth': '🔥', 'Hunger': '🍖', 'Health': '❤️', 'Sanity': '🧠', 'Stamina': '⚡'}
    
    for stat_name, icon in stat_icons.items():
        value = player.stats[stat_name]
        bar = create_bar(value)
        embed.add_field(
            name=f"{icon} {stat_name}",
            value=f"{bar} {value}%",
            inline=False
        )
    
    # Информация о локации и действии
    embed.add_field(
        name="📍 Location",
        value=f"X: {player.xCoord}, Y: {player.yCoord}",
        inline=False
    )
    
    embed.add_field(
        name="⏱️ Cooldown",
        value=f"{player.cooldown}s" if player.cooldown > 0 else "None",
        inline=True
    )
    
    embed.set_footer(text="Game Statistics • Updated in real-time")
    
    return embed


'''async def tick(user_id): #данная функция запускается тактовым генератором для каждого объекта player. она проверяет ряд значений полей объекта, изменяет их. выглядит неэффективно, определённо требует оптимизации

    player = player_dict[user_id]

    # ОПТИМИЗИРОВАТЬ
    if player.stats['Warmth']//10 != (player.stats['Warmth'] + player.modifiers['Warmth'])//10: await update_stat_display(user_id, 'Warmth')
    if player.stats['Hunger']//10 != (player.stats['Hunger'] + player.modifiers['Hunger'])//10: await update_stat_display(user_id, 'Hunger')
    if player.stats['Health']//10 != (player.stats['Health'] + player.modifiers['Health'])//10: await update_stat_display(user_id, 'Health')
    if player.stats['Sanity']//10 != (player.stats['Sanity'] + player.modifiers['Sanity'])//10: await update_stat_display(user_id, 'Sanity')
    if player.stats['Stamina']//10 != (player.stats['Stamina'] + player.modifiers['Stamina'])//10: await update_stat_display(user_id, 'Stamina')

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
    player.set_modifiers('Strength', 10) #VARIABLE

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
            player.set_modifiers('Stamina', 20) #0.8
        case Action.BREAKDOWN:
            pass
        case Action.KNOCKEDOUT:
            player.set_modifiers('Stamina', 0.07)  

    if player.stats['Warmth']>100: player.set_stats('Warmth', 100)
    if player.stats['Hunger']>100: player.set_stats('Hunger', 100)
    if player.stats['Health']>100: player.set_stats('Health', 100)
    if player.stats['Sanity']>100: player.set_stats('Sanity', 100)
    if player.stats['Stamina']>100: player.set_stats('Stamina', 100)
'''