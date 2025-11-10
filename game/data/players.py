from enum import Enum
from random import randint
from game.data.items import Tags

player_dict = {}

class Condition(Enum):
    ENCUMBERED = 1
    BURNING = 2
    BLEEDING = 3
    POISONED = 4
    DRUGGED = 5

class Action(Enum):
    BUILDING = 1
    FIGHTING = 2
 #   FLEEING = 3
    LOOTING = 4
    HIDING = 5
    RESTING = 6
    SLEEPING = 7
    BREAKDOWN = 8
 #   FAKING_DEAD = 9
 #   FAKING_KNOCKEDOUT = 10
    KNOCKEDOUT = 11

class Traits(Enum):
    A = 1
    B = 2

class Player:
    def __init__(self, builder):
        self.name = builder.name
        self.avatar = builder.avatar
        self.text_channel_id = builder.text_channel_id
        self.voice_channel_id = builder.voice_channel_id
        self.traits = builder.traits

        self.xCoord = builder.xCoord
        self.yCoord = builder.yCoord
        self.inventory = builder.inventory
        self.equipment = builder.equipment
        self.action = builder.action
        self.ticks = builder.ticks
        self.cooldown = builder.cooldown
        self.active = builder.active

        self.stats = builder.stats
        self.maxWeight = builder.maxWeight
        self.modifiers = builder.modifiers
        self.conditions = builder.conditions

        self.display = builder.display
        self.map = builder.map

    def set_text_channel(self, id): self.text_channel_id = id
    def set_voice_channel(self, id): self.voice_channel_id = id
    def set_traits(self, traits): self.traits = traits
    def set_xCoord(self, xCoord): self.xCoord = xCoord
    def set_yCoord(self, yCoord): self.yCoord = yCoord

    def add_item(self, item, value): self.inventory.update({item : value})
    def set_item(self, item, value): self.inventory[item] = value
    def remove_item(self, item): self.inventory.pop(item)

    def set_equipment(self, slot, equipment): self.equipment[slot] = equipment
    def set_action(self, action): self.action = action

    def set_ticks(self, ticks): self.ticks = ticks
    def add_ticks(self, ticks): self.ticks += ticks

    def set_cooldown(self, cooldown): self.cooldown = cooldown
    def add_cooldown(self, cooldown): self.cooldown += cooldown

    def set_stats(self, stat, value): self.stats[stat] = value
    def add_stats(self, stat, value): self.stats[stat] += value

    def set_maxWeight(self, maxWeight): self.maxWeight = maxWeight
    def set_modifiers(self, mod, value): self.modifiers[mod] = value
    def add_modifiers(self, mod, value): self.modifiers[mod] += value
    def set_conditions(self, conditions): self.conditions = conditions

    def set_map(self, xCoord, yCoord, emoji): self.map[xCoord][yCoord] = emoji
    def set_display_channel_id(self, category, index, new_id): self.display[category]['channels'][index] = new_id

class PlayerBuilder:
    def __init__(self):

        self.name = None
        self.avatar = None
        self.text_channel_id = None        
        self.voice_channel_id = None
        self.traits = []
        self.xCoord = None
        self.yCoord = None
        self.inventory = dict()
        self.equipment = {
            Tags.CLOTHES: None,
            Tags.MELEE: None,
            Tags.RANGED: None
        }
        self.action = None
        self.ticks = 0
        self.cooldown = -1
        self.active = True
        self.stats = {
            'Warmth': 100,
            'Hunger': 100,
            'Health': 100,
            'Sanity': 100,
            'Stamina': 100,
            'Weight': 0
        }
        self.maxWeight = 5
        self.modifiers = {
            'Warmth': 0,
            'Hunger': 0,
            'Health': 0,
            'Sanity': 0,
            'Stamina': 0,
            'Strength': 0
        }
        self.conditions = []
        self.display = None,
        self.map = []
        for i in range(5):
            self.map.append(['🌫️']*5)

    def with_name(self, name: str):
        self.name = name
        return self

    def with_avatar(self, avatar: str):
        self.avatar = avatar
        return self
    
    def with_channel(self, channel: int):
        self.text_channel_id = channel
        return self
    
    def with_display(self, display: dict):
        self.display = display
        return self

    def build(self):
        return Player(self)

def add_player(player):
    player_dict.update(player)

def remove_player(user_id):
    player_dict.pop(user_id)

def set_player(user_id, new_data):
    global player_dict
    player_dict[user_id] = new_data
