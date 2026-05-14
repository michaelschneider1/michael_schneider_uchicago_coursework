"""
CMSC 14100
Winter 2025
Homework #6

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

#############################################################################
#                                                                           #
# Important note: some of the tasks in this assignment have task-specific   #
# requirements/restrictions concerning the language constructs that you are #
# allowed to use in your solution. See the assignment writeup for details.  #
#                                                                           #
#############################################################################


# Constants
PLAYER_CLASSES = {"KNIGHT", "MAGE", "THIEF"}
LEVEL_LIMITS = [10,20,35,50,100,150, 200, 250, 500]

# Exercise 1
def validate_recipe(recipe):
    """
    Check if the given crafting recipe is valid. A crafting recipe is valid if
    it has a positive integer level, a valid player class, either: one 
    material with more than one quantity or two different materials with at 
    least one quantity each, and a positive integer power.

    Input:
        recipe (dict[str,Any]): a recipe dict

    Output (bool): True if recipe is valid, False if not.
    """
    if 'name' in recipe == False:
        return False
    
    power = recipe.get('power')
    level = recipe.get('level')
    if type(power) is not int or type(level) is not int:
        return False
    if power < 0 or level < 0:
        return False
    
    if recipe.get('class') not in PLAYER_CLASSES:
        return False
    
    materials_dict = recipe.get('materials')
    total = 0
    for resource in materials_dict:
        total += materials_dict.get(resource)
    if total < 2:
        return False
    
    return True

# Exercise 2.
def can_craft(recipe, player):
    """
    Check if the given player has the required level and class to craft the
    given recipe.

    Input:
        recipe (dict[str,Any]): a recipe dict
        player (dict[str,Any]): a player dict

    Output (bool): True if recipe is craftable by the player, False if not.
    """
    player_level = player.get('level')
    recipe_level = recipe.get('level')
    if player_level < recipe_level:
        return False

    player_class = player.get('class')
    recipe_class = recipe.get('class')
    if player_class != recipe_class:
        return False
    
    return True

# Exercise 3.
def filter_level_class(recipes, player):
    """
    Given a list of recipes, produce a list of recipes that are valid for the
    given player (i.e. the player has the required class and level). Does not 
    check if the player has the materials to craft the recipe.

    Input:
        recipe (list[dict[str,Any]]): a list of recipe dicts
        player (dict[str,Any]): a player dict
    Output (list[dict[str,Any]]): a list of recipes that the player can craft
        based solely on their level and class
    """
    final_list = []
    for recipe in recipes:
        if can_craft(recipe, player):
            final_list.append(recipe)
    return final_list

# Exercise 4.
def filter_recipe_materials(recipes, materials_set):
    """
    Given a set of materials, produce a list that contains only those recipes 
    that require only the materials in the given set.

    Input:
        recipe (list[dict[str,Any]]): a list of recipe dicts
        materials (set[str]): a set of materials

    Output (list[dict[str,Any]]): a list of recipes that the player can craft
        based on the materials in the set
    """
    final_list = []

    for recipe in recipes:
        recipe_materials = set(recipe.get('materials', ()))
        if recipe_materials.issubset(materials_set):
            final_list.append(recipe)
    return final_list

# Exercise 5.
def calculate_inventory_weight(player):
    """
    Given an inventory dict, compute the weight of all items in the inventory 
    and add it to the player dict. The weight of every item is 1.0

    Input:
        player (dict[str, Any]): a player dict

    Output: None
    """
    inventory = player.get('inventory')
    weight = 0

    for item in inventory:
        weight += inventory.get(item)
    player['total_weight'] = weight

# Exercise 6.
def add_items_to_inventory(player, items):
    """
    Given a player and a list of items, add the given items to the player's 
    inventory as long as the limit for the player's class is not reached and
    return the number of items that were added.

    Input 
        player (dict[str, Any]): a player dict
        items (list[str]): a list of items to add to the inventory

    Output (int): the number of items added to the inventory
    """
    items_added = 0
    player_inventory = player['inventory']
    for item in items:
        if item not in player_inventory:
            player_inventory[item] = 1
        else:
            player_inventory[item] += 1
        items_added += 1
    calculate_inventory_weight(player)
    return items_added



# Exercise 7.
def all_craftable_items(recipes, player):
    """
    Given a list of recipes and a player dictionary, produce a list of all 
    recipes that the given player is able to craft with their current level,
    class, and materials on hand.

    Input:
        recipes (list[dict[str,Any]]): list of recipe dictionaries
        player (dict[str,Any]): player dictionary

    Output (list[dict[str,Any]]): a list of recipes that the player can craft
        with their level, class, and materials
    """
    final_list = []
    player_materials = player.get('inventory', {})

    for recipe in recipes:
        recipe_materials = recipe.get('materials', {})
        has_sufficent_materials = True

        if can_craft(recipe, player) == False:
            continue
        
        for material, material_amount in recipe_materials.items():
            if (material not in player_materials or player_materials[material] 
            < material_amount):
                has_sufficent_materials = False
                break
        
        if has_sufficent_materials:
            final_list.append(recipe)
    
    return final_list

# Exercise 8.
def craft_max_power(recipes, player):
    """
    Given a list of recipes and a player dictionary, craft an item with the 
    greatest power from the given list of recipes that the player is able to
    craft given their class, level, and materials in their inventory.

    If successful, the materials in the inventory should be consumed and the 
    crafted item should be placed in the player's inventory. The power of the
    crafted item should be produced as output.

    Input:
        recipes (list[dict[str,Any]]): list of recipe dictionaries
        player (dict[str,Any]): player dictionary

    Output (int): The power of the crafted item if successful, and 0 otherwise
    """
    craftable_recipes = all_craftable_items(recipes, player)

    if craftable_recipes == []:
        return 0
    
    most_powerful_recipe = craftable_recipes[0]
    for recipe in craftable_recipes:
        if recipe.get('power') > most_powerful_recipe.get('power'):
            most_powerful_recipe = recipe
    
    for material, amount in most_powerful_recipe['materials'].items():
        player['inventory'][material] -= amount
        if player['inventory'][material] == 0:
            del player['inventory'][material]

    item_name = most_powerful_recipe.get('name')
    player['inventory'][item_name] = player['inventory'].get(item_name, 0) + 1
    calculate_inventory_weight(player)

    return most_powerful_recipe.get('power')