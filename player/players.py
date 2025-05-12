import json
from enum import Enum

class Condition(Enum):
    ENCUMBERED = 1
    BURNING = 2
    BLEEDING = 3
    POISONED = 4

class Action(Enum):
    BUILDING = 1
    FIGHTING = 2
    LOOTING = 3
 #   HIDING = 4
    RESTING = 5
    SLEEPING = 6
    BREAKDOWN = 7
 #   FAKING_DEAD = 8 
 #   FAKING_KNOCKEDOUT = 9
    KNOCKEDOUT = 10

class Traits(Enum):
    A = 1
    B = 2

class Player:
    def __init__(
        self, 
        user: tuple, #discord user
        name: str, 
        text_channel_id: int, #каждому игроку генерируется личный текстовый канал для написания команд
        voice_channel_id: int, 
        traits: list, 
        xCoord: int, 
        yCoord: int,  
        inventory: list, 
        action: Action, 
        ticks: int, 
        cooldown: int,
        active: bool,
        stats: dict,
#        statWarmth, 
#        statHunger, 
#        statHealth, 
#        statSanity, 
#        statStamina, 
#        statWeight, 
        maxWeight: float,
        modifiers: dict, 
#        modWarmth, 
#        modHunger, 
#        modHealth, 
#        modSanity, 
#        modStamina, 
#        modStrength, 
        conditions: list
    ):
        self.user = user
        self.name = name
        self.text_channel_id = text_channel_id
        self.voice_channel_id = voice_channel_id
        self.traits = traits

        self.xCoord = xCoord
        self.yCoord = yCoord
        self.inventory = inventory
        self.action = action
        self.ticks = ticks
        self.cooldown = cooldown
        self.active = active

        self.stats = stats
        self.maxWeight = maxWeight
        self.modifiers = modifiers
        self.conditions = conditions

# self.cooldown = int((16-self.statStrength)*0.5) UNIVERSAL COOLDOWN        

# далее не до конца реализованные механики, пока без документации

#    self.active = self.action != Action.SLEEPING and self.action != Action.KNOCKEDOUT and self.cooldown == -1

    def loot(self):
        if self.active:
            self.ticks=int((16-self.statStrength)+5) 
            self.action = Action.LOOTING
        else: message()

    def give(self, player, object):
        if self.active:
            pass
        else: message()

    def search_player(self, player):
        if self.active:
            pass
        else: message()

    def craft(self, object):
        if self.active:
            pass
        else: message()

    def use(self, object, action):
        if self.active:
            pass
        else: message()

    def attack(self, player):
        if self.active:
            self.action = Action.FIGHTING
        else: message()

    def rest(self):
        if self.active:
            self.action = Action.RESTING
        else: message()

    async def sleep(self):
        if self.active:
            self.action = Action.SLEEPING
            await self.user.edit(mute=True)
            await self.user.edit(deafen=True)
        else: message()

    async def wake_up(self): # later

        if self.action == Action.SLEEPING:
            if self.statStamina >= 60:
                self.action = Action.RESTING
                self.cooldown = int((16-self.statStrength)*0.5)
                await self.user.edit(mute=False)
                await self.user.edit(deafen=False)

        elif self.action == Action.KNOCKEDOUT:
            self.action = Action.RESTING
            self.cooldown = int((16-self.statStrength)*0.5)
            if type(self.xCoord)==int and type(self.yCoord)==int:
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                if len(board[self.xCoord][self.yCoord].players)==1:
                    board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type)
                move_to_vc(board[self.xCoord][self.yCoord].channel)
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                self.voice_channel_id = board[self.xCoord][self.yCoord].channel
            else:
                for player in player_list:
                    if ((int(self.xCoord)+1>player.xCoord>int(self.xCoord) and self.yCoord==player.yCoord) or (int(self.yCoord)+1>player.yCoord>int(self.yCoord) and self.xCoord==player.xCoord)) and player.action not in ['hiding','sleeping','knockedout','faking_sleeping','faking_knockedout','faking_dead']:
                        move_to_vc(player.voice_channel_id)
                        self.voice_channel_id = delete_channel(self.voice_channel_id)
                        self.voice_channel_id = player.voice_channel_id
                        break

    def die():
        pass
    def quit():
        pass

player_dict = dict() #temporary

def add_player(user_id, name, channel):
    player_dict.update({ user_id : {
            'name' : name,
            'text_channel_id' : channel,
            'voice_channel_id' : None,
            'traits' : [],
            'xCoord' : None,
            'yCoord' : None,  
            'inventory' : [], 
            'action' : None,
            'ticks' : 0,
            'cooldown' : -1,
            'active' : True,
            'stats' : {
                'Warmth' : 100,
                'Hunger' : 100,
                'Health' : 100,
                'Sanity' : 100,
                'Stamina' : 100,
                'Weight' : 0
            },
            'maxWeight' : 5,
            'modifiers' : {
                'Warmth' : 0,
                'Hunger' : 0,
                'Health' : 0,
                'Sanity' : 0,
                'Stamina' : 0,
                'Strength' : 0
            },
            'conditions' : []
        }})  

def remove_player(user):
    player_list.pop(find_player(user)) 
'''
def find_player(name):
    for i in range(len(player_list)):
        if player_list[i].name==name:
            return i
'''

def fetch_player(user):
    with open('player/player_list.json') as f:

        player_list = json.load(f)

        for player in player_list:
            if player['user_id'] == user.id: return player
    
    return None