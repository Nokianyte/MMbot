from bot.client import discord, app_commands, client, tree
from game.data.players import player_dict, Action, remove_player
from game.data.map import board
from game.data.values import GAME_PACE, LOBBY_CHANNEL_ID, SLEEPING_ROLE_ID, ATTACKING_ROLE_ID
from game.functions import start_game, update_stat_display
from ui.select_menus import *
from utils.helpers import load_profile, remove_role, delete_channel, move_to_vc, close_active_menu, register_menu, on_cooldown

@tree.command(
    name="profile",
    description="check profile",
    guild=discord.Object(id=1370677493685817344)
)
async def profile(ctx):
    await ctx.response.send_message(view=ProfileView(user_id=ctx.user.id, user_data=load_profile(ctx.user.id)), ephemeral=True)

@tree.command(
    name="start_game",
    description="must be in a voice channel",
    guild=discord.Object(id=1370677493685817344)
)
@app_commands.choices(choices=[
    app_commands.Choice(name=key, value=value) for key, value in GAME_PACE.items()
])
async def start(ctx, choices: app_commands.Choice[int]):
    await ctx.response.defer(ephemeral=True)
    await start_game(ctx, choices.value)
    await ctx.followup.send('Игра началась!', ephemeral=True)


@tree.command(
    name="quit",
    description="quits the game",
    guild=discord.Object(id=1370677493685817344)
)
async def leave(ctx):

    user = ctx.user.id
    player = player_dict[user]
    tile = board[player.xCoord][player.yCoord]

    player.set_text_channel(await delete_channel(player.text_channel_id))
    remove_player(user)
    tile.remove_player(user)

    await move_to_vc(ctx, int(user), None)

    if len(tile.players) == 0:
        tile.set_channel(await delete_channel(tile.channel))

    for id in player.display['🗺️']['channels'].values():
        await delete_channel(id)

    await delete_channel(player.display['🗺️']['category_id'])

    for id in player.display['🩻']['channels'].values():
        await delete_channel(id)

    await delete_channel(player.display['🩻']['category_id'])

    lobby_channel = client.get_channel(LOBBY_CHANNEL_ID)

    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = True

    await lobby_channel.set_permissions(ctx.user, overwrite = overwrite)

@tree.command(
    name="i",
    description="inventory",
    guild=discord.Object(id=1370677493685817344)
)
@close_active_menu
async def inventory(ctx, action: str = None, item_name: str = None):
    print(item_name, action)
    if player_dict[ctx.user.id].inventory != {}:
        if item_name != None and action != None:
            print('a')
            await handle_direct_action(ctx, item_name, action)
            return
        player_dict[ctx.user.id].set_action(Action.RESTING)
        await ctx.response.send_message(view=InventoryView(ctx=ctx))
        message = await ctx.original_response()
        register_menu(ctx.user.id, message)
    else:
        await ctx.response.send_message("Your inventory is empty", ephemeral=True)

@tree.command(
    name="a",
    description="action",
    guild=discord.Object(id=1370677493685817344)
)
@close_active_menu
async def action(ctx):
    await ctx.response.send_message(view=ActionView(ctx=ctx))
    message = await ctx.original_response()
    register_menu(ctx.user.id, message)

@tree.command(
    name="m",
    description="move between tiles",
    guild=discord.Object(id=1370677493685817344)
)
@close_active_menu
@on_cooldown
async def move(ctx):
    player_dict[ctx.user.id].set_action(Action.RESTING)
    if player_dict[ctx.user.id].stats['Stamina'] >70: 
        await ctx.response.send_message(view=MoveView(ctx=ctx))
        message = await ctx.original_response()
        register_menu(ctx.user.id, message)
    else: 
        await ctx.response.send_message("Too low on stamina!", ephemeral=True)
            
@tree.command(
    name="wake_up",
    description="wake up",
    guild=discord.Object(id=1370677493685817344)
)
async def wake_up(ctx):
    await remove_role(ctx, ctx.user.id, SLEEPING_ROLE_ID)
    await ctx.user.edit(mute=False, deafen=False)
    player_dict[ctx.user.id].set_action(Action.RESTING)

    await ctx.response.send_message("You woke up!", ephemeral=True)

@tree.command(
    name="attack",
    description="attack player",
    guild=discord.Object(id=1370677493685817344)
)
@close_active_menu
@on_cooldown
async def attack(ctx):
    if len(board[player_dict[ctx.user.id].xCoord][player_dict[ctx.user.id].yCoord].players) < 2:
        await ctx.response.send_message(content="No valid targets!", ephemeral=True)
        return  

    await ctx.response.send_message(view=PlayerView(ctx=ctx, action="attack"))
    message = await ctx.original_response()
    register_menu(ctx.user.id, message)

@tree.command(
    name="flee",
    description="run from fight",
    guild=discord.Object(id=1370677493685817344)
)
@on_cooldown
async def flee(ctx):
    player_dict[ctx.user.id].set_action(Action.RESTING)
    player_dict[ctx.user.id].set_cooldown(player_dict[ctx.user.id].cooldown + 3)
    player_dict[ctx.user.id].set_stats('Stamina', player_dict[ctx.user.id].stats['Stamina'] - 10)
    await remove_role(ctx, ctx.user.id, ATTACKING_ROLE_ID)

    await ctx.response.send_message("You fled from the fight!", ephemeral=True)

@tree.command(
    name="block",
    description="block incoming damage",
    guild=discord.Object(id=1370677493685817344)
)
@on_cooldown
async def block(ctx):

    await ctx.response.send_message("You fled from the fight!", ephemeral=True)


async def handle_direct_action(ctx, item_name: str, action: str):
    """Обрабатывает прямые действия типа '/inventory ramen eat'"""
    player = player_dict[ctx.user.id]
    
    # Проверяем, есть ли предмет в инвентаре
    if item_name not in player.inventory:
        await ctx.response.send_message(f"You don't have '{item_name}' in your inventory", ephemeral=True)
        return
    
    item = ITEMS_DICT[item_name]
    
    # Проверяем, доступно ли действие для этого предмета
    available_actions = get_available_actions(item, player)
    
    if action.lower() not in available_actions:
        await ctx.response.send_message(
            f"Action '{action}' is not available for {item_name}. Available actions: {', '.join(available_actions)}",
            ephemeral=True
        )
        return
    
    # Выполняем действие
    await execute_item_action(ctx, item_name, action.lower())
    unregister_menu(ctx.user.id)

def get_available_actions(item, player) -> list:
    """Возвращает список доступных действий для предмета"""
    actions = []
    
    if Tags.FOOD == item.tags: 
        actions.append("eat")
    if Tags.CONSUMABLE == item.tags: 
        actions.append("consume")
    if Tags.STORAGE == item.tags: 
        actions.append("equip")
    if Tags.CLOTHES == item.tags: 
        if player.equipment[Tags.CLOTHES] == item.name: 
            actions.append("unequip")
        else: 
            actions.append("equip")
    if Tags.MELEE == item.tags: 
        if player.equipment[Tags.MELEE] == item.name: 
            actions.append("unequip")
        else: 
            actions.append("equip")
    if Tags.RANGED == item.tags: 
        if player.equipment[Tags.RANGED] == item.name: 
            actions.append("unequip")
        else: 
            actions.append("equip")
        actions.append("unload")
    if Tags.AMMO == item.tags: 
        actions.append("load")
    if Tags.TRAP == item.tags: 
        actions.append("place")
    if Tags.UTILITY == item.tags: 
        actions.append("use")
    
    actions.extend(["give", "throw"])
    
    return actions

async def execute_item_action(ctx, item_name: str, action: str):
    """Выполняет действие с предметом"""
    player = player_dict[ctx.user.id]
    item = ITEMS_DICT[item_name]
    
    match action:
        case "eat":
            if Tags.FOOD != item.tags:
                await ctx.response.send_message(f"Cannot eat {item_name}", ephemeral=True)
                return
                
            player.set_stats("Hunger", player.stats["Hunger"] + item.value)
            player.set_item(item_name, player.inventory[item_name] - 1)
            await update_stat_display(ctx.user.id, 'Hunger')
            
            if player.inventory[item_name] == 0: 
                player.remove_item(item_name)
                await ctx.response.send_message(f"You ate {item_name} and replenished your hunger")
            else:
                await ctx.response.send_message(f"You ate {item_name} and replenished your hunger")
                
        case "equip":
            player.set_equipment(item.tags, item_name)
            await ctx.response.send_message(f"Equipped {item_name}")
            
        case "unequip":
            player.set_equipment(item.tags, None)
            await ctx.response.send_message(f"Unequipped {item_name}")
            
        case "consume":
            # Добавьте логику для consume
            await ctx.response.send_message(f"Consumed {item_name}")
            
        case "use":
            # Добавьте логику для use
            await ctx.response.send_message(f"Used {item_name}")
            
        case "give":
            if len(board[player.xCoord][player.yCoord].players) > 1:
                await ctx.response.send_message(view=PlayerView(ctx=ctx, action="give", item_name=item_name))
            else:
                await ctx.response.send_message(content="No valid targets!", ephemeral=True)
                
        case "throw":
            player.set_item(item_name, player.inventory[item_name] - 1)
            if player.inventory[item_name] == 0: 
                player.remove_item(item_name)
            await ctx.response.send_message(f"Threw away {item_name}")
            
        case _:
            await ctx.response.send_message(f"Action '{action}' is not implemented for direct execution", ephemeral=True)