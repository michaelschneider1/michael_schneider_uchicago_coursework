from hw7 import Item, Player

# Constants
JUNK_VALUE = 1
CURRENCY = "Gold"
ALL_CLASSES = {"Warrior", "Knight", "Blacksmith", "Mage"}

# Crafting Recipes
sword_recipe = {"Iron Ingot": 2, "Wood": 1}

# Items
def get_sword():
    return Item(name="Sword", power=20, allowed_classes={
                "Warrior", "Knight"}, weight=5.0, durability=5, value=50, recipe=sword_recipe)

def get_ingot():
    return Item(name="Iron Ingot", power=0, allowed_classes={
                "Blacksmith", "Warrior"}, weight=2.0, durability=1, value=10)

def get_wood():
    return Item(name="Wood", power=0, allowed_classes={
            "Blacksmith", "Warrior"}, weight=1.0, durability=1, value=5)

# Currency
def get_gold():
    return Item(name="Gold", power=0, allowed_classes=ALL_CLASSES, weight=0.5, durability=1, value=1)
    

# Players
def get_mage():
    return Player(name="Gandalf", player_class="Mage")

def get_warrior():
    return Player(name="Aragorn", player_class="Warrior")

def get_warrior_2():
    return Player(name="Legolas", player_class="Warrior")
