"""
CMSC 14100
Winter 2025
Homework #7

We will be using anonymous grading, so please do NOT include your name
in this file.

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.

"""

"""
1) price() in the Item class changed the if <bool> == False to if  not <bool>
to improve code quality (line 90)
2) add_item() and get_item() of Inventory class changed to store the the item 
name as the key of the inventory dictionary [changed other functions to keep up
with this model]
3) buy_item() updated to use has_items to check if the items are in inventory
(line 258, 260)
4) changed sell_item to call buy item to reduce repeated code
"""
# CONSTANTS
JUNK_VALUE = 1
CURRENCY = "Gold"
ALL_CLASSES = {"Warrior", "Knight", "Blacksmith", "Mage"}

class Item:
    """Represents an item that can be used, crafted, or picked up."""

    def __init__(self, name, power, allowed_classes, weight, durability, value, recipe=None):
        """
        Constructor for Item.

        Args:
            name: (str): The name of the item.
            power: (int): The power of the item.
            allowed_classes: (set): The set of player classes that can use the item.
            weight: (float): The weight of the item.
            durability: (int): The durability of the item.
            value: (int): The value of the item in gold coins.
            recipe: (dictionary): The recipe for crafting the item, default is 
                                  None for an item that is not crafted
        """
        self.name = name
        self.power = power
        self.allowed_classes = allowed_classes
        self.weight = weight
        self.durability = durability
        self.value = value
        self.recipe = recipe or {}

    def use(self):
        """
        Reduces durability when used and returns whether the item is still usable.

        Args:
            None

        Returns:
            boolean, True if the item is still usable, False otherwise.
        """
        if self.durability > 1:
            self.durability -= 1
            return True
        if self.durability == 1:
            print(f"{self.name} has broken!")
            self.durability -= 1
            return False
        if self.durability == 0:
            print(f"{self.name} is broken and cannot be used")
            return False
        return True

    def price(self):
        """
        Returns the current price of the item. If the item's durability is 
        0, it's value is JUNK_VALUE.

        Returns:
            int: The items actual value, or 1 if the item is broken.
        """
        if not Item.use(self):
            return JUNK_VALUE
        return self.value

    def __repr__(self):
        """
        Generates string representation of the object
        """
        return f"<{self.name} : ${self.value}>"


class Inventory:
    """Represents a player's inventory, managing items and their quantities."""

    def __init__(self):
        """
        Constructor for Inventory
        """
        self.inventory = {}
    
    def add_item(self, item, quantity=1):
        """
        Adds an item to the inventory, increasing its quantity if already present.

        Args:
            item: (Item), The item to be added.
            quantity: (int), The quantity of the item to be added, default is 1.

        Returns:
            None
        """
        if item.name not in self.inventory:
            self.inventory[item.name] = (item, quantity)
        else:
            existing_item, existing_quantity = self.inventory[item.name]
            self.inventory[item.name] = (existing_item, existing_quantity + \
                                         quantity)

    def get_item(self, item_name):
        """
        Returns the item object and quantity from the inventory. Returns
        (None, None) if item is not present.

        Args:
            item_name (str): Name of the item to check
        Returns:
            tuple(Item, int): The Item object and quantity in this inventory
        """
        return self.inventory.get(item_name, (None, None))

    def total_weight(self):
        """
        Calculates the total weight of items in the inventory.

        Returns:
            (float), The total weight of items in the inventory.
        """
        total_weight = 0
        for item_info in self.inventory.values():
            item, item_quantity = item_info
            total_weight += item_quantity * item.weight
        return total_weight
    
    def has_items(self, manifest):
        """
        Checks if the inventory contains the required items for crafting.

        Args:
            manifest: (dict), The manifest of required item names and their quantities.

        Returns:
            (boolean), True if the inventory contains the required items, False otherwise.
        """
        for item_name, required_quantity in manifest.items():
            if item_name not in self.inventory:
                return False
            _, available_quantity = self.inventory[item_name]
            if available_quantity < required_quantity:
                return False
        return True

    def remove_items(self, manifest):
        """
        Removes required items from the inventory after crafting.

        Args:
            manifest: (dict), The manifest of item names and their quantities to remove

        Returns:
            None
        """
        for item_name, remove_quantity in manifest.items():
            if item_name in self.inventory:
                item, quantity = self.inventory[item_name]
                updated_quantity = quantity - remove_quantity
                if updated_quantity <= 0:
                    del self.inventory[item_name]
                else:
                    self.inventory[item_name] = (item, updated_quantity)

class Player:
    """Represents a player with attributes such as health, XP, and inventory."""

    def __init__(self, name, player_class):
        """
        Constructor for Player class.

        Args:
            name: str, The name of the player.
            player_class: str, The class of the player.

        Returns:
            None
        """
        self.name = name
        self.player_class = player_class
        self.health = 100
        self.inventory = Inventory()

    def pick_up_item(self, item, quantity=1):
        """
        Allows the player to pick up an item if their class allows it,
        adding it to their inventory.

        Args:
            item: Item, The item to be picked up.
            quantity: int, The quantity of the item to be picked up, default is 1.

        Returns:
            bool: True if item(s) were picked up, False otherwise
        """
        if self.player_class not in item.allowed_classes:
            return False
        else:
            self.inventory.add_item(item, quantity)
            return True

    def craft_item(self, item):
        """
        Crafts an item if the player has the necessary materials in their inventory.

        Args:
            item: Item, The item to be crafted.

        Returns:
            bool: True if item was crafted, False otherwise
        """
        if self.inventory.has_items(item.recipe):
            self.inventory.add_item(item, 1)
            self.inventory.remove_items(item.recipe)
            return True
        return False

    def buy_item(self, item_name, quantity, other_player):
        """
        Allows the player to buy an item from another player in exchange for gold.
        
        Inputs:
            item_name (str): Name of the item to be bought
            quantity (int): Quantity to be bought
            other_player (Player): Player to buy from

        Outputs:
            (bool): True if sale is successful, False if not
        """
        gold_item, gold_quantity = self.inventory.get_item(CURRENCY)
        item, _ = other_player.inventory.get_item(item_name)
        
        if not other_player.inventory.has_items({item_name: quantity}):
            return False
        if not self.inventory.has_items({CURRENCY: gold_quantity}):
            return False
        price = item.value * quantity
        if (gold_quantity >= price and self.player_class in 
        item.allowed_classes):
            self.inventory.add_item(item, quantity)
            self.inventory.remove_items({CURRENCY: price})
            other_player.inventory.add_item(gold_item, price)
            other_player.inventory.remove_items({item_name: quantity})
            return True
        return False
        

    def sell_item(self, item_name, quantity, other_player):
        """
        Allows the player to sell an item to a player for gold.
        
        Inputs:
            item_name (str): Name of the item to be sold
            quantity (int): Quantity to be sold
            other_player (Player): Player to sell to

        Outputs:
            (bool): True if sale is successful, False if not
        """
        return other_player.buy_item(item_name, quantity, self)

    def __repr__(self):
        """
        Representation of the player.

        Args:
            None

        Returns:
            string, The name of the player.
        """
        return self.name