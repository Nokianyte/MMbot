class Room:
    def __init__(
            self, 
            channel: tuple, 
            Type: enumerate, 
            terrain_bonus: int, 
            xCoord: int, 
            yCoord: int, 
            loot: list, 
            content: list, 
            players: list, 
            entities: list, 
            burning: bool
            ):
                
        self.channel = channel #голосовой канал
        self.Type = Type
        self.terrain_bonus = terrain_bonus
        self.yCoord = yCoord
        self.xCoord = xCoord
        self.loot = loot
        self.content = content
        self.entities = entities
        self.players = players
        self.burning = burning

board = [] #двухмерный массив из объектов класса Room. Индексы - координаты комнаты

#Изначально планировалось, чтобы игрок мог передвигаться буквально между "клетками", имея при этом дробные координаты, но в связи с ненужными сложностями, данную фичу собираюсь убрать

