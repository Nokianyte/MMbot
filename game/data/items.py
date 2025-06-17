from enum import Enum

class Tags(Enum):
    FOOD = 1
    CONSUMABLE = 2
    STORAGE = 3
    CLOTHES = 4
    TOOL = 5
    MELEE = 6
    RANGED = 7
    AMMO = 8
    TRAP = 9
    RESOURSE = 10
    UTILITY = 11
    OTHER = 12

class ItemClass:
    def __init__(self, emoji: str, description: str, tags: Tags, value: int, weight: float):
        self.emoji=emoji
        self.description=description
        self.tags=tags
        self.value=value
        self.weight=weight

ITEMS_DICT = {

    "Berries" : ItemClass(
        emoji = "🫐",
        description = "Better than nothing",
        tags = Tags.FOOD,
        value = 1,
        weight = 0
    ),
    "Mushroom" : ItemClass(
        emoji = "🍄‍🟫",
        description = "Might replenish a bit of hunger",
        tags = Tags.FOOD,
        value = 2,
        weight = 0
    ),
    "Canned soup" : ItemClass(
        emoji = "🥫",
        description = "Where's the opener?",
        tags = Tags.FOOD,
        value = 20,
        weight = 0.3
    ),
    "Ramen" : ItemClass(
        emoji = "🥡",
        description = "Cheap and simple",
        tags = Tags.FOOD,
        value = 10,
        weight = 0.3
    ),
    "Raw meat" : ItemClass(
        emoji = "🥩",
        description = "Should probably cook it",
        tags = Tags.FOOD,
        value = 10,
        weight = 0.3
    ),
    "Cooked meat" : ItemClass(
        emoji = "🍖",
        description = "Delicious steak",
        tags = Tags.FOOD,
        value = 30,
        weight = 0.3
    ),
    "Fish" : ItemClass(
        emoji = "🐟",
        description = "Scrumptious water creature",
        tags = Tags.FOOD,
        value = 10,
        weight = 0.2
    ),
    "Cooked fish" : ItemClass(
        emoji = "🍣",
        description = "Sushi???",
        tags = Tags.FOOD,
        value = 30,
        weight = 0.2
    ),
    "Antibiotics" : ItemClass(
        emoji = "💊",
        description = "Cure from poison",
        tags = Tags.CONSUMABLE,
        value = 0,
        weight = 0.1
    ),
    "Painkillers" : ItemClass(
        emoji = "💊",
        description = "Those don`t heal but numb the pain",
        tags = Tags.CONSUMABLE,
        value = 0,
        weight = 0.1
    ),
    "Bandage" : ItemClass(
        emoji = "🧻",
        description = "Best way to stop bleeding",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.1
    ),
    "Suitcase" : ItemClass(
        emoji = "💼",
        description = "Smaller container",
        tags = Tags.STORAGE,
        value = 5,
        weight = 0.3
    ),
    "Backpack" : ItemClass(
        emoji = "🎒",
        description = "Bigger container",
        tags = Tags.STORAGE,
        value = 15,
        weight = 1
    ),
    "Warm clothes" : ItemClass(
        emoji = "🧥",
        description = "Must-have in this enviroment",
        tags = Tags.CLOTHES,
        value = 20,
        weight = 1
    ),
    "Ice ax" : ItemClass(
        emoji = "⛏️",
        description = "Used mostly for climbing",
        tags = Tags.MELEE,
        value = 0,
        weight = 0.5
    ),
    "Pocket knife" : ItemClass(
        emoji = "🔪",
        description = "A compact multitool",
        tags = Tags.MELEE,
        value = 0,
        weight = 0.2
    ),
    "Axe" : ItemClass(
        emoji = "🪓",
        description = "Trees be damned",
        tags = Tags.MELEE,
        value = 0,
        weight = 1
    ),
    "Wooden club" : ItemClass(
        emoji = "🪈",
        description = "Bonk",
        tags = Tags.MELEE,
        value = 0,
        weight = 0.5
    ),
    "Pistol" : ItemClass(
        emoji = "🔫",
        description = "Deadly firearm",
        tags = Tags.RANGED,
        value = 0,
        weight = 0.5
    ),
    "Rifle" : ItemClass(
        emoji = "🔫",
        description = "Deadlier firearm",
        tags = Tags.RANGED,
        value = 0,
        weight = 1
    ),
    "Bow" : ItemClass(
        emoji = "🏹",
        description = "Improvised shooter",
        tags = Tags.RANGED,
        value = 0,
        weight = 0.5
    ),
    "Pistol ammo" : ItemClass(
        emoji = "🔩",
        description = "Don`t forget to load them in",
        tags = Tags.AMMO,
        value = 0,
        weight = 0.1
    ),
    "Rifle ammo" : ItemClass(
        emoji = "🔩",
        description = "Don't forget to load them in",
        tags = Tags.AMMO,
        value = 0,
        weight = 0.1
    ),
    "Arrow" : ItemClass(
        emoji = "🥢",
        description = "Cheap ammo for cheap weapon",
        tags = Tags.AMMO,
        value = 0,
        weight = 0.1
    ),
    "Rope" : ItemClass(
        emoji = "🪢",
        description = "Might be used for restraining",
        tags = Tags.TRAP,
        value = 0,
        weight = 0.2
    ),
    "Beartrap" : ItemClass(
        emoji = "🕳",
        description = "Better watch your steps",
        tags = Tags.TRAP,
        value = 0,
        weight = 1
    ),
    "Wood" : ItemClass(
        emoji = "🪵",
        description = "Common crafting material",
        tags = Tags.RESOURSE,
        value = 0,
        weight = 0.3
    ),
    "Stone" : ItemClass(
        emoji = "🪨",
        description = "Less useful crafting material",
        tags = Tags.RESOURSE,
        value = 0,
        weight = 0.3
    ),
    "Cloth" : ItemClass(
        emoji = "🗞",
        description = "Might need something to put it all together",
        tags = Tags.RESOURSE,
        value = 0,
        weight = 0.1
    ),
    "Sewing kit" : ItemClass(
        emoji = "🪡",
        description = "Can sew all kinds of tissue together",
        tags = Tags.RESOURSE,
        value = 0,
        weight = 0.1
    ),
    "Walkie-talkie" : ItemClass(
        emoji = "📟",
        description = "Allows distant communication",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.2
    ),
    "Flashlight" : ItemClass(
        emoji = "🔦",
        description = "Guidence in the darkness",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.2
    ),
    "Lighter" : ItemClass(
        emoji = "🕯",
        description = "Essential for survival",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.1
    ),
    "Molotov" : ItemClass(
        emoji = "🍾",
        description = "Careful with that",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.3
    ),
    "Bottle" : ItemClass(
        emoji = "🍾",
        description = "Container for liquids",
        tags = Tags.OTHER,
        value = 0,
        weight = 0.2
    ),
    "Book of rituals" : ItemClass(
        emoji = "📓",
        description = "Some secrets cost a price",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.3
    ),
    "Binoculars" : ItemClass(
        emoji = "🥽",
        description = "Used to see further in more detail",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.2
    ),
    "Signal flare" : ItemClass(
        emoji = "🧨",
        description = "Best way to attract attention",
        tags = Tags.UTILITY,
        value = 0,
        weight = 0.2
    )
}