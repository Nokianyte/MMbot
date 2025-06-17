from random import randint, choice, sample
from utils.helpers import create_vc, move_to_vc

MAP_SIZE = 5

SPAWN_COORDS = {"xCoord" : 0, "yCoord" : 0}

ITEMS_SPAWN_AMMOUNT = 20

board = []

class Tile:
    def __init__(self, builder):               
        self.channel = builder.channel #голосовой канал
        self.terrain = builder.terrain
        self.emoji = builder.emoji
        self.terrain_bonus = builder.terrain_bonus
        self.structure = builder.structure
        self.loot = builder.loot
        self.content = builder.content
        self.players = builder.players

    def set_channel(self, id): self.channel = id
    def set_terrain(self, terrain): self.terrain = terrain
    def set_terrain(self, emoji): self.emoji = emoji
    def set_terrain_bonus(self, terrain_bonus): self.terrain_bonus = terrain_bonus
    def set_structure(self, structure): self.structure = structure

    def append_loot(self, loot): self.loot.append(loot)
    def set_loot(self, loot): self.loot = loot
    def remove_loot(self, loot): self.loot.remove(loot)

    def set_content(self, content): self.content = content
    def set_players(self, players): self.players = players

    def append_player(self, player): self.players.append(player)
    def remove_player(self, player): self.players.remove(player)


class TileBuilder:
    def __init__(self):
        self.channel = None
        self.terrain = "Grove"
        self.emoji = None
        self.terrain_bonus = 0
        self.structure = None
        self.loot = []
        self.content = []
        self.players = []


    def with_coords(self, xCoord, yCoord):
        neighbours = []

        if xCoord > 0: neighbours.append(set(TILE_TYPES[board[xCoord - 1][yCoord].terrain]['neighbours']))
        else: neighbours.append(set(TILE_TYPES[board[MAP_SIZE - 1][yCoord].terrain]['neighbours']))

        if xCoord < MAP_SIZE -1 : neighbours.append(set(TILE_TYPES[board[xCoord + 1][yCoord].terrain]['neighbours']))
        else: neighbours.append(set(TILE_TYPES[board[0][yCoord].terrain]['neighbours']))

        if yCoord > 0: neighbours.append(set(TILE_TYPES[board[xCoord][yCoord - 1].terrain]['neighbours']))
        else: neighbours.append(set(TILE_TYPES[board[xCoord][MAP_SIZE - 1].terrain]['neighbours']))

        if yCoord < MAP_SIZE - 1: neighbours.append(set(TILE_TYPES[board[xCoord][yCoord + 1].terrain]['neighbours']))
        else: neighbours.append(set(TILE_TYPES[board[xCoord][0].terrain]['neighbours']))

        intersec = set.intersection(*neighbours)

        self.terrain = sample(list(intersec), 1)[0]
        terrain = TILE_TYPES[self.terrain]

        self.structure, structure = choice(list(STRUCTURES.items()))

        self.emoji = terrain['emoji'] + structure['emoji'] + terrain['emoji']

        self.loot = list(terrain['loot'].keys()) + list(structure['loot'].keys())

        return self
    
    def build(self):
        return Tile(self)
    
def generate_board():
    for x in range(MAP_SIZE):
        board.append(list())

    for x in range(MAP_SIZE):       
        for y in range(MAP_SIZE):
            board[x].append(TileBuilder().build())

    for x in range(MAP_SIZE): 
        for y in range(MAP_SIZE):
            board[x][y] = TileBuilder().with_coords(x, y).build()

async def spawn_players(ctx, player_dict):

    xSpawn = SPAWN_COORDS['xCoord']
    ySpawn = SPAWN_COORDS['yCoord']

    spawn_point = board[xSpawn][ySpawn]

    spawn_point.channel = await create_vc(ctx, spawn_point.emoji)

    for user_id, player in player_dict.items():
        spawn_point.append_player(user_id)
        player.set_xCoord(xSpawn) 
        player.set_yCoord(ySpawn)
        player.set_voice_channel(spawn_point.channel)
        await move_to_vc(ctx, user_id, spawn_point.channel)

def set_board(new_board):
    global board
    board = new_board

TILE_TYPES = {
    "Thicket" : {
        "emoji" : "🌲",
        "neighbours" : [
            "Thicket",
            "Grove",
            "Cliffs"
        ],
        "loot" : {
            "Berries": 0,
            "Mushroom": 0,
            "Wood": 0
        }
    },
    "Grove" : {
        "emoji" : "🌿",
        "neighbours" : [
            "Grove",
            "Thicket",
            "Meadow",
            "Cliffs"
        ],
        "loot" : {
            "Berries": 0,
            "Mushroom": 0,
            "Wood": 0
        }
    },
    "Meadow" : {
        "emoji" : "🌾",
        "neighbours" : [
            "Meadow",
            "Grove"
        ],
        "loot" : {}
    },
    "Cliffs" : {
        "emoji" : "🗻",
        "neighbours" : [
            "Cliffs",
            "Thicket",
            "Grove"
        ],
        "loot": {
            "Stone": 0
        }
    }
}

STRUCTURES = {
    "Tent" : {
        "emoji" : "⛺️",
        "rarity": 0,
        "loot": {
            "Pistol": 0,
            "Pistol ammo": 0,
            "Antibiotics": 0,
            "Painkillers": 0,
            "Canned soup": 0,
            "Ramen": 0,
            "Bandage": 0,
            "Backpack": 0,
            "Warm clothes": 0,
            "Ice ax": 0,
            "Pocket knife": 0,
            "Cloth": 0,
            "Sewing kit": 0,
            "Walkie-talkie": 0,
            "Flashlight": 0,
            "Lighter": 0,
            "Bottle": 0,
            "Binoculars": 0,
            "Signal flare": 0
        }
    },
    "Grave" : {
        "emoji" : "🪦",
        "rarity": 0,
        "loot": {
            "Book of rituals": 0,
            "Ice ax": 0,
            "Pocket knife": 0,
            "Cloth": 0,
            "Lighter": 0,
            "Bottle": 0
        }
    },
    "Shack" : {
        "emoji" : "🛖",
        "rarity": 0,
        "loot": {
            "Rifle": 0,
            "Rifle ammo": 0,
            "Pistol": 0,
            "Pistol ammo": 0,
            "Book of rituals": 0,
            "Axe": 0,
            "Canned soup": 0,
            "Ramen": 0,
            "Bandage": 0,
            "Backpack": 0,
            "Warm clothes": 0,
            "Ice ax": 0,
            "Pocket knife": 0,
            "Cloth": 0,
            "Sewing kit": 0,
            "Lighter": 0,
            "Bottle": 0,
            "Binoculars": 0
        }
    },
    "Supplies" : {
        "emoji" : "🗃",
        "rarity": 0,
        "loot": {
            "Pistol ammo": 0,
            "Rifle ammo": 0,
            "Antibiotics": 0,
            "Painkillers": 0,
            "Canned soup": 0,
            "Ramen": 0,
            "Bandage": 0,
            "Warm clothes": 0,
            "Ice ax": 0,
            "Cloth": 0,
            "Sewing kit": 0,
            "Walkie-talkie": 0,
            "Flashlight": 0,
            "Lighter": 0,
            "Binoculars": 0,
            "Signal flare": 0
        }
    },
    "Plane debries" : {
        "emoji" : "🛩",
        "rarity": 0,
        "loot": {
            "Canned soup": 0,
            "Ramen": 0,
            "Antibiotics": 0,
            "Painkillers": 0,
            "Bandage": 0,
            "Suitcase": 0,
            "Backpack": 0,
            "Warm clothes": 0,
            "Cloth": 0,
            "Flashlight": 0,
            "Binoculars": 0
        }
    }
}



    

