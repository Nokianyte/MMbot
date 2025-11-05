from bot.client import discord
from game.data.avatar import AVATAR_DICT
from game.data.players import player_dict, Action
from game.data.map import board, MAP_SIZE
from game.data.items import Tags, ITEMS_DICT
from game.data.values import SLEEPING_ROLE_ID, ATTACKING_ROLE_ID
from game.functions import update_stat_display, update_map
from utils.helpers import overwrite_profile, unregister_menu, give_role, remove_role, create_vc, move_to_vc, delete_channel, message

class Profile(discord.ui.Select):
    def __init__(self, user_id, user_data):

        self.user_id = user_id
        self.user_data = user_data

        options=[
            discord.SelectOption(label="Avatar",emoji=AVATAR_DICT[user_data['avatar']['face']][user_data['avatar']['skin']][user_data['avatar']['hair']],description="Customize you avatar")
            ]
        super().__init__(placeholder="Edit profile",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Avatar":
            await interaction.response.edit_message(view=AvatarView(user_id=self.user_id, user_data=self.user_data))

class ProfileView(discord.ui.View):
    def __init__(self, *, timeout = 180, user_id, user_data):
        self.user_id = user_id
        self.user_data = user_data
        super().__init__(timeout=timeout)
        self.add_item(Profile(user_id=self.user_id, user_data=self.user_data))

# AVATAR

class Avatar(discord.ui.Select):
    def __init__(self, user_id, user_data):

        self.user_id = user_id
        self.user_data = user_data

        options=[
            discord.SelectOption(label="Face",emoji=AVATAR_DICT[user_data['avatar']['face']][0][6],description="Change face"),
            discord.SelectOption(label="Skin",emoji=AVATAR_DICT[user_data['avatar']['face']][user_data['avatar']['skin']][6],description="Change skin"),
            discord.SelectOption(label="Hair",emoji=AVATAR_DICT[user_data['avatar']['face']][0][user_data['avatar']['hair']],description="Change hair"),
            discord.SelectOption(label="Back",emoji="↩️")
            ]
        super().__init__(placeholder="Edit avatar",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Face":
            await interaction.response.edit_message(view=FaceView(user_id=self.user_id, user_data=self.user_data))
        if self.values[0] == "Skin":
            await interaction.response.edit_message(view=SkinView(user_id=self.user_id, user_data=self.user_data))
        if self.values[0] == "Hair":
            await interaction.response.edit_message(view=HairView(user_id=self.user_id, user_data=self.user_data))
        if self.values[0] == "Back":
            await interaction.response.edit_message(view=ProfileView(user_id=self.user_id, user_data=self.user_data))

class AvatarView(discord.ui.View):
    def __init__(self, *, timeout = 180, user_id, user_data):
        self.user_id = user_id
        self.user_data = user_data
        super().__init__(timeout=timeout)
        self.add_item(Avatar(user_id=self.user_id, user_data=self.user_data))



class Face(discord.ui.Select):
    def __init__(self, user_id, user_data):

        self.user_id = user_id
        self.user_data = user_data

        options=[
            discord.SelectOption(label=key,emoji=value[user_data['avatar']['skin']][user_data['avatar']['hair']]) for key, value in AVATAR_DICT.items()
            ]
        super().__init__(placeholder="Select face",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        self.user_data['avatar']['face'] = int(self.values[0])
        overwrite_profile(user_id=self.user_id, new_data=self.user_data)
        await interaction.response.edit_message(view=AvatarView(user_id=self.user_id, user_data=self.user_data))

class FaceView(discord.ui.View):
    def __init__(self, *, timeout = 180, user_id, user_data):
        self.user_id = user_id
        self.user_data = user_data
        super().__init__(timeout=timeout)
        self.add_item(Face(user_id=self.user_id, user_data=self.user_data))




class Skin(discord.ui.Select):
    def __init__(self, user_id, user_data):

        self.user_id = user_id
        self.user_data = user_data

        options=[
            discord.SelectOption(label=key,emoji=value[user_data['avatar']['hair']]) for key, value in AVATAR_DICT[user_data['avatar']['face']].items() if key!=0
            ]
        super().__init__(placeholder="Select skin",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        self.user_data['avatar']['skin'] = int(self.values[0])
        overwrite_profile(user_id=self.user_id, new_data=self.user_data)
        await interaction.response.edit_message(view=AvatarView(user_id=self.user_id, user_data=self.user_data))

class SkinView(discord.ui.View):
    def __init__(self, *, timeout = 180, user_id, user_data):
        self.user_id = user_id
        self.user_data = user_data
        super().__init__(timeout=timeout)
        self.add_item(Skin(user_id=self.user_id, user_data=self.user_data))



class Hair(discord.ui.Select):
    def __init__(self, user_id, user_data):

        self.user_id = user_id
        self.user_data = user_data

        options=[
            discord.SelectOption(label=key,emoji=value) for key, value in AVATAR_DICT[user_data['avatar']['face']][user_data['avatar']['skin']].items()
            ]
        super().__init__(placeholder="Select hair",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        self.user_data['avatar']['hair'] = int(self.values[0])
        overwrite_profile(user_id=self.user_id, new_data=self.user_data)
        await interaction.response.edit_message(view=AvatarView(user_id=self.user_id, user_data=self.user_data))

class HairView(discord.ui.View):
    def __init__(self, *, timeout = 180, user_id, user_data):
        self.user_id = user_id
        self.user_data = user_data
        super().__init__(timeout=timeout)
        self.add_item(Hair(user_id=self.user_id, user_data=self.user_data))


#IN-GAME

class ActionSelect(discord.ui.Select):
    def __init__(self, ctx):

        self.ctx = ctx
        self.player = player_dict[ctx.user.id]

        options=[
            discord.SelectOption(label="Loot",emoji="🔎",description="Search for items"),
            discord.SelectOption(label="Sleep",emoji="😴",description="Replenish stamina"),
            discord.SelectOption(label="Rest",emoji="🔥",description="Replenish stamina"),
            discord.SelectOption(label="Cancel",emoji="↩️")
            ]
        super().__init__(placeholder="Select action",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):

        unregister_menu(self.ctx.user.id)

        match self.values[0]:
            case "Loot":
                self.player.set_action(Action.LOOTING)
                await interaction.response.edit_message(content="Looting...",view=None)
                self.player.set_ticks(2)

            case "Sleep":
                await give_role(self.ctx, self.ctx.user.id, SLEEPING_ROLE_ID)
                await self.ctx.user.edit(mute=True, deafen=True)
                self.player.set_action(Action.SLEEPING)
                await interaction.response.edit_message(content="Sleeping...",view=None)

            case "Rest":
                self.player.set_action(Action.RESTING)
                await interaction.response.edit_message(content="Resting...",view=None)

            case "Cancel":
                await interaction.response.edit_message(content="Interaction cancelled!", view=None)
                await interaction.delete_original_response()
                return

class ActionView(discord.ui.View):
    def __init__(self, *, timeout = 60, ctx):
        self.ctx = ctx
        super().__init__(timeout=timeout)
        self.add_item(ActionSelect(ctx=self.ctx))



class Move(discord.ui.Select):

    global player_dict
    global board
    global MAP_SIZE

    def __init__(self, ctx):

        self.ctx = ctx
        self.player = player_dict[ctx.user.id]

        if self.player.yCoord < len(board)-1: north_emoji = board[self.player.xCoord][self.player.yCoord + 1].emoji[0]
        else: north_emoji = board[self.player.xCoord][0].emoji[0]

        if self.player.yCoord > 0: south_emoji = board[self.player.xCoord][self.player.yCoord - 1].emoji[0]
        else: south_emoji = board[self.player.xCoord][MAP_SIZE - 1].emoji[0]

        if self.player.xCoord < len(board)-1: east_emoji = board[self.player.xCoord + 1][self.player.yCoord].emoji[0]
        else: east_emoji = board[0][self.player.yCoord].emoji[0]

        if self.player.xCoord > 0: west_emoji = board[self.player.xCoord - 1][self.player.yCoord].emoji[0]
        else: west_emoji = board[MAP_SIZE - 1][self.player.yCoord].emoji[0]

        options=[
            discord.SelectOption(label="North",emoji=north_emoji),
            discord.SelectOption(label="South",emoji=south_emoji),
            discord.SelectOption(label="East",emoji=east_emoji),
            discord.SelectOption(label="West",emoji=west_emoji),
            discord.SelectOption(label="Cancel",emoji="↩️")
            ]
        super().__init__(placeholder="Select direction",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):

        unregister_menu(interaction.user.id)

        old_tile = board[self.player.xCoord][self.player.yCoord]

        match self.values[0]:
            case "North":
                if self.player.yCoord < len(board)-1:
                    new_tile = board[self.player.xCoord][self.player.yCoord + 1]
                    self.player.set_yCoord(self.player.yCoord + 1)
                else: 
                    new_tile = board[self.player.xCoord][0]
                    self.player.set_yCoord(0)
            case "South":
                if self.player.yCoord > 0:
                    new_tile = board[self.player.xCoord][self.player.yCoord - 1]
                    self.player.set_yCoord(self.player.yCoord - 1)
                else: 
                    new_tile = board[self.player.xCoord][MAP_SIZE - 1]
                    self.player.set_yCoord(MAP_SIZE - 1)
            case "East":
                if self.player.xCoord < len(board)-1:
                    new_tile = board[self.player.xCoord + 1][self.player.yCoord]
                    self.player.set_xCoord(self.player.xCoord + 1)
                else: 
                    new_tile = board[0][self.player.yCoord]
                    self.player.set_xCoord(0)
            case "West":
                if self.player.xCoord > 0:
                    new_tile = board[self.player.xCoord - 1][self.player.yCoord]
                    self.player.set_xCoord(self.player.xCoord - 1)
                else: 
                    new_tile = board[MAP_SIZE - 1][self.player.yCoord]
                    self.player.set_xCoord(MAP_SIZE - 1)
            case "Cancel":
                await interaction.response.edit_message(content="Movement cancelled!", view=None)
                await interaction.delete_original_response()
                return

        await interaction.response.edit_message(content=f"Moved {self.values[0]}", view=None)

        old_tile.remove_player(self.ctx.user.id)

        if len(new_tile.players) == 0:
            channel = await create_vc(self.ctx, new_tile.emoji)
            new_tile.set_channel(channel)

        new_tile.append_player(self.ctx.user.id)

        await move_to_vc(self.ctx, self.ctx.user.id, new_tile.channel)

        if len(old_tile.players) == 0:
            old_tile.set_channel(await delete_channel(old_tile.channel))

        self.player.set_stats('Stamina', self.player.stats['Stamina'] - 60)
        #await update_stat_display(self.ctx.user.id, 'Stamina')
        await update_map(self.ctx.user.id)

class MoveView(discord.ui.View):
    def __init__(self, *, timeout = 60, ctx):
        self.ctx = ctx
        super().__init__(timeout=timeout)
        self.add_item(Move(ctx=self.ctx))



class Inventory(discord.ui.Select):
    def __init__(self, ctx):

        self.ctx = ctx
        self.player = player_dict[ctx.user.id]

        options=[
            discord.SelectOption(label=f"{item} [{ammount}]",value=item,emoji=ITEMS_DICT[item].emoji,description=ITEMS_DICT[item].description) for item, ammount in self.player.inventory.items()
            ]
        options.append(discord.SelectOption(label="Back",emoji="↩️"))

        super().__init__(placeholder="Inventory",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "Back":
            unregister_menu(self.ctx.user.id)
            await interaction.response.edit_message(content="Interaction cancelled!", view=None)
            await interaction.delete_original_response()
            return

        await interaction.response.edit_message(view=ItemView(ctx=self.ctx, item_name=self.values[0]))

class InventoryView(discord.ui.View):
    def __init__(self, *, timeout = 60, ctx):
        self.ctx = ctx
        super().__init__(timeout=timeout)
        self.add_item(Inventory(ctx=self.ctx))



class ItemSelect(discord.ui.Select):
    def __init__(self, ctx, item_name):

        self.ctx = ctx
        self.item_name = item_name
        self.item = ITEMS_DICT[item_name]
        self.player = player_dict[ctx.user.id]

        options=[]

        if Tags.FOOD == self.item.tags: 
            options.append(discord.SelectOption(label="Eat",emoji="🗣"))
        if Tags.CONSUMABLE == self.item.tags: 
            options.append(discord.SelectOption(label="Consume",emoji="🗣"))
        if Tags.STORAGE == self.item.tags: 
            options.append(discord.SelectOption(label="Equip",emoji="👜"))
        if Tags.CLOTHES == self.item.tags: 
            if self.player.equipment[Tags.CLOTHES] == item_name: options.append(discord.SelectOption(label="Unequip",emoji="👕"))
            else: options.append(discord.SelectOption(label="Equip",emoji="👕"))
        if Tags.MELEE == self.item.tags: 
            if self.player.equipment[Tags.MELEE] == item_name: options.append(discord.SelectOption(label="Unequip",emoji="🗡"))
            else: options.append(discord.SelectOption(label="Equip",emoji="🗡"))
        if Tags.RANGED == self.item.tags: 
            if self.player.equipment[Tags.RANGED] == item_name: options.append(discord.SelectOption(label="Unequip",emoji="🔫"))
            else: options.append(discord.SelectOption(label="Equip",emoji="🔫"))
            options.append(discord.SelectOption(label="Unload",emoji="🔫"))
        if Tags.AMMO == self.item.tags: 
            options.append(discord.SelectOption(label="Load",emoji="🔫"))
        if Tags.TRAP == self.item.tags: 
            options.append(discord.SelectOption(label="Place",emoji="🕳"))
        if Tags.UTILITY == self.item.tags: 
            options.append(discord.SelectOption(label="Use",emoji="🕳"))

        options.append(discord.SelectOption(label="Give",emoji="🫴"))
        options.append(discord.SelectOption(label="Throw away",emoji="⤵️"))
        options.append(discord.SelectOption(label="Back",emoji="↩️"))

        super().__init__(placeholder=f"{self.item.emoji} {self.item_name} [{self.player.inventory[self.item_name]}]",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):

        match self.values[0]:
            case "Back":
                await interaction.response.edit_message(content=None, view=InventoryView(ctx=self.ctx))
                return
            case "Give":
                if len(board[self.player.xCoord][self.player.yCoord].players) > 1:
                    await interaction.response.edit_message(view=PlayerView(ctx=self.ctx, action="give"))
                else:
                    await interaction.response.send_message(content="No valid targets!", ephemeral=True)
                return               
            case "Eat":
                self.player.set_stats("Hunger", self.player.stats["Hunger"] + self.item.value)
                self.player.set_item(self.item_name, self.player.inventory[self.item_name] - 1)
                await update_stat_display(self.ctx.user.id, 'Hunger')
                if self.player.inventory[self.item_name] == 0: 
                    self.player.remove_item(self.item_name)
                    await interaction.response.edit_message(content="You have replenished your hunger", view=InventoryView(ctx=self.ctx))
                else:
                    await interaction.response.edit_message(content="You have replenished your hunger", view=ItemView(ctx=self.ctx, item_name=self.item_name))
            case "Equip":
                self.player.set_equipment(self.item.tags, self.item_name)
                await interaction.response.edit_message(content=f"Equiped {self.item_name}", view=ItemView(ctx=self.ctx, item_name=self.item_name))
            case "Unequip":
                self.player.set_equipment(self.item.tags, None)
                await interaction.response.edit_message(content=f"Unequipped {self.item_name}", view=ItemView(ctx=self.ctx, item_name=self.item_name))

class ItemView(discord.ui.View):
    def __init__(self, *, timeout = 60, ctx, item_name):
        self.ctx = ctx
        self.item_name = item_name
        super().__init__(timeout=timeout)
        self.add_item(ItemSelect(ctx=self.ctx, item_name=self.item_name))




class PlayerSelect(discord.ui.Select):
    def __init__(self, ctx, action):

        self.ctx = ctx
        self.action = action
        self.player = player_dict[ctx.user.id]

        options=[discord.SelectOption(label=player_dict[player].name,value=player,emoji=player_dict[player].avatar) for player in board[self.player.xCoord][self.player.yCoord].players if player != ctx.user.id]

        options.append(discord.SelectOption(label="Cancel",value=0,emoji="↩️"))

        super().__init__(placeholder="Select target",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):

        target = int(self.values[0])

        if target == 0:
            unregister_menu(self.ctx.user.id)
            await interaction.response.edit_message(content="Interaction cancelled!", view=None)
            await interaction.delete_original_response()
            return
        
        match self.action:

            case "give":
                pass

            case "attack":
                self.player.set_action(Action.FIGHTING)
                await give_role(self.ctx, self.ctx.user.id, ATTACKING_ROLE_ID)

                """
                if player_dict[target].action == Action.SLEEPING:

                    await remove_role(self.ctx, target, SLEEPING_ROLE_ID)
                    await ctx.user.edit(mute=False, deafen=False)
                    player_dict[ctx.user.id].set_action(Action.RESTING)
                """

                player_dict[target].set_action(Action.FIGHTING)
                await give_role(self.ctx, target, ATTACKING_ROLE_ID)

                await message(target, f"You are attacked by {self.ctx.user.name}!")
                player_dict[target].set_stats('Health', player_dict[target].stats['Health'] - player_dict[target].modifiers['Strength']) #later
                await update_stat_display(target, 'Health')
                player_dict[target].set_cooldown(player_dict[target].cooldown + 3)
                self.player.set_cooldown(self.player.cooldown + 4)
                self.player.set_stats('Stamina', self.player.stats['Stamina'] - 5)
                await update_stat_display(self.ctx.user.id, 'Health')

                await interaction.response.edit_message(content=f"You attacked {player_dict[target].name}!", view=None)
                unregister_menu(self.ctx.user.id)

class PlayerView(discord.ui.View):
    def __init__(self, *, timeout = 60, ctx, action):
        self.ctx = ctx
        self.action = action
        super().__init__(timeout=timeout)
        self.add_item(PlayerSelect(ctx=self.ctx, action=self.action))