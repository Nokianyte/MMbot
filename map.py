class Room:
    def __init__(self, channel, Type, terrain_bonus, xCoord, yCoord, loot, content, players, entities, burning):
        self.channel = channel
        self.Type = Type
        self.terrain_bonus = terrain_bonus
        self.yCoord = yCoord
        self.xCoord = xCoord
        self.loot = loot
        self.content = content
        self.entities = entities
        self.players = players
        self.burning = burning

board = []

