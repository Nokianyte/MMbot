from bot.client import discord, app_commands, client, tree
from game.data.players import player_dict, Action, remove_player
from game.data.map import board
from game.data.values import GAME_PACE, LOBBY_CHANNEL_ID, SLEEPING_ROLE_ID, ATTACKING_ROLE_ID
from game.functions import start_game
from ui.select_menus import *
from utils.helpers import load_profile, remove_role, delete_channel, move_to_vc, no_concurrent, on_cooldown

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

    lobby_channel = client.get_channel(LOBBY_CHANNEL_ID)

    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = True

    await lobby_channel.set_permissions(ctx.user, overwrite = overwrite)

@tree.command(
    name="stats",
    description="view stats",
    guild=discord.Object(id=1370677493685817344)
)
async def stats(ctx):
    player = player_dict[ctx.user.id]
    await ctx.response.send_message(f"## 🧠 `{int(player.stats['Sanity'])}`\n## 👅 `{int(player.stats['Hunger'])}`\n## 🫀 `{int(player.stats['Health'])}`\n## 🫁 `{int(player.stats['Stamina'])}`\n## 🌡 `{int(player.stats['Warmth'])}`",ephemeral=True)

@tree.command(
    name="inventory",
    description="check inventory",
    guild=discord.Object(id=1370677493685817344)
)
@no_concurrent
async def inventory(ctx):
    if player_dict[ctx.user.id].inventory != {}:
        player_dict[ctx.user.id].set_action(Action.RESTING)
        await ctx.response.send_message(view=InventoryView(ctx=ctx))
    else:
        await ctx.response.send_message("Your inventory is empty", ephemeral=True)
        lock_in(ctx)

@tree.command(
    name="action",
    description="action",
    guild=discord.Object(id=1370677493685817344)
)
@no_concurrent
async def action(ctx):
    await ctx.response.send_message(view=ActionView(ctx=ctx))

@tree.command(
    name="move",
    description="between tiles",
    guild=discord.Object(id=1370677493685817344)
)
@no_concurrent
@on_cooldown
async def move(ctx):
    player_dict[ctx.user.id].set_action(Action.RESTING)
    if player_dict[ctx.user.id].stats['Stamina'] >70: await ctx.response.send_message(view=MoveView(ctx=ctx))
    else: 
        await ctx.response.send_message("Too low on stamina!", ephemeral=True)
        lock_in(ctx)
            
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
@no_concurrent
@on_cooldown
async def attack(ctx):
    if len(board[player_dict[ctx.user.id].xCoord][player_dict[ctx.user.id].yCoord].players) < 2:
        await ctx.response.send_message(content="No valid targets!", ephemeral=True)
        lock_in(ctx)
        return  

    await ctx.response.send_message(view=PlayerView(ctx=ctx, action="attack"))

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