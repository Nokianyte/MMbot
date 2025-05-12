import json

class Tile:
    def __init__(
            self, 
            channel: tuple, 
            Type: enumerate, 
            terrain_bonus: int,  
            loot: list, 
            content: list, 
            players: list
            ):
                
        self.channel = channel #голосовой канал
        self.Type = Type
        self.terrain_bonus = terrain_bonus
        self.loot = loot
        self.content = content
        self.players = players

def generate_map():
    with open('map/board.json', 'w') as f:
        json.dump([ 
            [{"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}], 
            [{"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}], 
            [{"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}], 
            [{"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}], 
            [{"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}, {"channel" : None, "type" : "Поле", "terrain_bonus" : 0, "content" : None, "loot" : [], "players" : []}] 
        ], f)

