class Item:
    def __init__(self, name, id, type, char, weight):
        self.name=name
        self.id=id
        self.type=type
        self.char=char
        self.weight=weight

item_list = [

    Item('Консервированная тушёнка',0,'food',20,0.3),
    Item('Консервированные овощи',1,'food',10,0.3),
    Item('Сухпаёк',2,'food',10,0.1),
    Item('Мясо животного',3,'food',10,0.3),
    Item('Жаренное мясо животного',4,'food',30,0.3),
    Item('Рыба',5,'food',10,0.2),
    Item('Жаренная рыба',6,'food',30,0.2),
    Item('Человеческое мясо',7,'food',10,0.3),
    Item('Жаренное человеческое мясо',8,'food',30,0.3),

    Item('Антибиотики',9,'consumable',None,0.1),
    Item('Бинты',10,'consumable',None,0.1),
    Item('Алкоголь',11,'consumable',None,0.3),

    Item('Маленький рюкзак',12,'storage',5,0.3),
    Item('Походный рюкзак',13,'storage',15,1),

    Item('Тёплая одежда',14,'clothes',20,1),
    Item('Камуфляж',15,'clothes',5,0.5),

    Item('Ледоруб',16,'weapon',None,0.5),
    Item('Складной нож',17,'weapon',None,0.2),
    Item('Топор',18,'weapon',None,1),
    Item('Деревянный кол',19,'weapon',None,0.5),

    Item('Пистолет',20,'gun',None,0.5),
    Item('Ружье',21,'gun',None,1),
    Item('Винтовка',22,'gun',None,1),
    Item('Самодельный лук',23,'gun',None,0.5),

    Item('Пистолетный патрон',24,'ammo',None,0.1),
    Item('Ружейный патрон',25,'ammo',None,0.1),
    Item('Винтовочный патрон',26,'ammo',None,0.1),
    Item('Самодельная стрела',27,'ammo',None,0.2),

    Item('Сеть',28,'trap',None,0.2),
    Item('Капкан',29,'trap',None,1),

    Item('Древисина',30,'resource',None,0.3),
    Item('Камень',31,'resource',None,0.3),
    Item('Шкура',32,'resource',None,0.3),
    Item('Ткань',33,'resource',None,0.1),

    Item('Швейные принадлежности',34,'other',None,0.1),
    Item('Компас',35,'other',None,0.2),
    Item('Рация',36,'other',None,0.2),
    Item('Батарейка',37,'other',None,0.1),
    Item('Фонарик',38,'other',None,0.2),
    Item('Зажигалка',39,'other',None,0.1),
    Item('Факел',40,'other',None,0.2),
    Item('Коктейль Молотова',41,'other',None,0.3),
    Item('Стеклянная бутылка',42,'other',None,0.2),
    Item('Справочник по выживанию',43,'other',None,0.2),
    Item('Книга Обрядов',44,'other',None,0.3),
    Item('Бензин',45,'other',None,0.5),
    Item('Бинокль',46,'other',None,0.2),
    Item('Сигнальный огонь',47,'other',None,0.2)

]