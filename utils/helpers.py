import json
from functools import wraps
from bot.client import discord, client
from game.data.players import player_dict

active_players = set()

def lock_in(ctx):
    active_players.discard(ctx.user.id)

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

async def message(user_id, message):

    global player_dict

    channel = client.get_channel(player_dict[user_id].text_channel_id)
    await channel.send(message)

async def give_role(ctx, user_id, role_id):
    role = ctx.guild.get_role(role_id)
    user = await ctx.guild.fetch_member(user_id)
    await user.add_roles(role)

async def remove_role(ctx, user_id, role_id):
    role = ctx.guild.get_role(role_id)
    user = await ctx.guild.fetch_member(user_id)
    await user.remove_roles(role)

def load_profile(user_id):

    f = open('game/user_profiles.json')
    user_dict = json.load(f)
    f.close()

    if str(user_id) not in list(user_dict.keys()):
        user_dict.update({str(user_id) : {"avatar" : {"face" : 2, "skin" : 1, "hair" : 1}}})

        with open('game/user_profiles.json', 'w') as f:
            json.dump(user_dict, f)

    return user_dict[str(user_id)]
    
def overwrite_profile(user_id, new_data):
    f = open('game/user_profiles.json')
    user_dict = json.load(f)
    user_dict[user_id] = new_data
    f.close()

    with open('game/user_profiles.json', 'w') as f:
        json.dump(user_dict, f)

def no_concurrent(func):

    global active_players
    
    @wraps(func)
    async def wrapper(ctx: discord.Interaction, *args, **kwargs):
        if ctx.user.id in active_players:
            await ctx.response.send_message(
                "Please wait until your current command completes!",
                ephemeral=True
            )
            return
            
        active_players.add(ctx.user.id)
                
        return await func(ctx, *args, **kwargs)

    return wrapper

def on_cooldown(func):
    
    global player_dict

    @wraps(func)
    async def wrapper(ctx: discord.Interaction, *args, **kwargs):
        if player_dict[ctx.user.id].cooldown > 0:
            await ctx.response.send_message(
                "You're out of breath!",
                ephemeral=True
            )
            return
                
        return await func(ctx, *args, **kwargs)

    return wrapper 