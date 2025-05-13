import json

board = []

class Tile:
    def __init__(
            self, 
            channel: tuple, 
            terrain: enumerate, 
            terrain_bonus: int,  
            loot: list, 
            content: list, 
            players: list
            ):
                
        self.channel = channel #голосовой канал
        self.terrain = terrain
        self.terrain_bonus = terrain_bonus
        self.loot = loot
        self.content = content
        self.players = players

def generate_map():

    return [ 
        [Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = [])], 
        [Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = [])], 
        [Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = [])], 
        [Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = [])], 
        [Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = []), Tile(channel = None, terrain = "Поле", terrain_bonus = 0, loot = [], content = [], players = [])] 
    ]

