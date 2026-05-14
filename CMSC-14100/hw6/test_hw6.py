"""
CMSC 14100
Updated Winter 2025

Test code for Homework #6
"""
import hw6

import os
import sys
import pytest
import helpers
import copy

# Input Data for tests
from load_data import load_recipes, load_invalid_recipes, load_players

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position

MODULE = "hw6"

basic_steps = [
    "from load_data import load_recipes, load_invalid_recipes, load_players"
]

crafting_recipes = load_recipes()
invalid_recipes = load_invalid_recipes()
players = load_players()

############################
# Tests for  validate_recipe
############################
@pytest.mark.parametrize("ix, recipe, expected", [(ix, r, True) for ix, r in enumerate(crafting_recipes)])
def test_validate_recipe(ix, recipe, expected):
    """ Test code for validate_recipe """
    steps = basic_steps + [
            f"crafting_recipes = load_recipes()"
            f"recipe = crafting_recipes[{ix}]",
            "hw6.validate_recipe(recipe)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw6.validate_recipe(recipe)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("ix, recipe, expected", [(ix, r, False) for ix, r in enumerate(invalid_recipes)])
def test_validate_recipe_invalid(ix, recipe, expected):
    """ Test code for validate_recipe """
    steps = basic_steps + [ "invalid_recipes = load_invalid_recipes()",
            f"recipe = invalid_recipes[{ix}]",
            "hw6.validate_recipe(recipe)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw6.validate_recipe(recipe)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

############################
# Tests for can_craft
############################

can_craft_data =[
    (0, 0, False),
    (0, 1, False),
    (0, 2, False),
    (0, 3, False),
    (0, 4, True),
    (0, 5, False),
    (0, 6, False),
    (1, 0, False),
    (1, 1, False),
    (1, 2, True),
    (1, 3, True),
    (1, 4, False),
    (1, 5, False),
    (1, 6, False),
    (2, 0, False),
    (2, 1, False),
    (2, 2, False),
    (2, 3, False),
    (2, 4, False),
    (2, 5, False),
    (2, 6, False),
    (3, 0, True),
    (3, 1, True),
    (3, 2, False),
    (3, 3, False),
    (3, 4, False),
    (3, 5, True),
    (3, 6, False),
    (4, 0, False),
    (4, 1, False),
    (4, 2, False),
    (4, 3, False),
    (4, 4, False),
    (4, 5, False),
    (4, 6, False),
]
@pytest.mark.parametrize("ix, jx, expected", can_craft_data)
def test_can_craft(ix, jx, expected):
    """ Test code for can_craft """
    steps = basic_steps + [ "players = load_players()",
                           "crafting_recipes = load_recipes()",
            f"player = players[{ix}]",
            f"recipe = crafting_recipes[{jx}]",
            "hw6.can_craft(recipe, player)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw6.can_craft(crafting_recipes[jx], players[ix])
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


##############################
# Tests for filter_level_class
##############################

filter_level_class_data = [
    (0, [{'name': 'staff', 'level': 3, 'class': 'MAGE', 'materials': {'wood': 2, 'string': 1}, 'power': 4}]),
(1, [{'name': 'sword', 'level': 3, 'class': 'KNIGHT', 'materials': {'wood': 2, 'iron': 2}, 'power': 7}, {'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}]),
(2, []),
(3, [{'name': 'axe', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 3, 'iron': 1}, 'power': 5}, {'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}, {'name': 'lockpick', 'level': 3, 'class': 'THIEF', 'materials': {'iron': 2}, 'power': 2}]),
(4, []),
]

@pytest.mark.parametrize("ix, expected", filter_level_class_data)
def test_filter_level_class(ix, expected):
    """ Test code for filter_level_class """
    steps = basic_steps + [ "players = load_players()",
                           "crafting_recipes = load_recipes()",
            f"player = players[{ix}]",
            "hw6.filter_level_class(crafting_recipes, player)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw6.filter_level_class(crafting_recipes, players[ix])
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    # TODO: Modify test to check unordered set of recipes, maybe or provide 
    # a ordering criteria in the problem specification
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


##############################
# Tests for filter_recipe_materials
##############################
filter_data = [
    (set(),[]),
({'wood'},[{'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}, {'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}]),
({'iron'},[{'name': 'lockpick', 'level': 3, 'class': 'THIEF', 'materials': {'iron': 2}, 'power': 2}]),
({'wood', 'iron'},[{'name': 'axe', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 3, 'iron': 1}, 'power': 5}, {'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}, {'name': 'sword', 'level': 3, 'class': 'KNIGHT', 'materials': {'wood': 2, 'iron': 2}, 'power': 7}, {'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}, {'name': 'lockpick', 'level': 3, 'class': 'THIEF', 'materials': {'iron': 2}, 'power': 2}]),
({'string', 'ivy', 'wood', 'clay', 'leaf', 'iron'},[{'name': 'axe', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 3, 'iron': 1}, 'power': 5}, {'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}, {'name': 'sword', 'level': 3, 'class': 'KNIGHT', 'materials': {'wood': 2, 'iron': 2}, 'power': 7}, {'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}, {'name': 'staff', 'level': 3, 'class': 'MAGE', 'materials': {'wood': 2, 'string': 1}, 'power': 4}, {'name': 'lockpick', 'level': 3, 'class': 'THIEF', 'materials': {'iron': 2}, 'power': 2}]),
({'water', 'wood', 'feather', 'leaf'},[{'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}, {'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}]),
({'water', 'string', 'feather', 'ivy', 'wood', 'leaf', 'iron'},[{'name': 'axe', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 3, 'iron': 1}, 'power': 5}, {'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}, {'name': 'sword', 'level': 3, 'class': 'KNIGHT', 'materials': {'wood': 2, 'iron': 2}, 'power': 7}, {'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}, {'name': 'staff', 'level': 3, 'class': 'MAGE', 'materials': {'wood': 2, 'string': 1}, 'power': 4}, {'name': 'lockpick', 'level': 3, 'class': 'THIEF', 'materials': {'iron': 2}, 'power': 2}]),
({'lockpick', 'axe', 'sword', 'plank', 'sheild', 'staff', 'potion'},[]),
]
@pytest.mark.parametrize("materials, expected", filter_data)
def test_filter_recipe_materials(materials, expected):
    """ Test code for filter_recipe_materials """
    steps = basic_steps + [ "players = load_players()",
                           "crafting_recipes = load_recipes()",
            f"materials = {materials}",
            "hw6.filter_recipe_materials(crafting_recipes, materials)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw6.filter_recipe_materials(crafting_recipes, materials)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



##############################
# Tests for calculate_inventory_weight
##############################

inventory_data = [
  (0, {'level': 3, 'class': 'MAGE', 'inventory': {'wood': 10, 'iron': 3, 'feathers': 1, 'string': 2}, 'total_weight': 16.0}),
(1, {'level': 4, 'class': 'KNIGHT', 'inventory': {'wood': 3, 'iron': 1, 'stone': 5}, 'total_weight': 9.0}),
(2, {'level': 1, 'class': 'THIEF', 'inventory': {'wood': 3, 'iron': 1}, 'total_weight': 4.0}),
(3, {'level': 6, 'class': 'THIEF', 'inventory': {'wood': 3, 'iron': 1}, 'total_weight': 4.0}),
(4, {'level': 0, 'class': 'THIEF', 'inventory': {'wood': 10}, 'total_weight': 10.0}),
]

@pytest.mark.parametrize("ix, expected", inventory_data)
def test_calculate_inventory_weight(ix, expected):
    """ Test code for calculate_inventory_weight """
    steps = basic_steps + [ "players = load_players()",
            f"player = players[{ix}]",
            "hw6.calculate_inventory_weight(player)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    player_copy = copy.deepcopy(players[ix])

    try:
        actual = hw6.calculate_inventory_weight(player_copy)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_none(actual, None)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_result(player_copy, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


##############################
# Tests for add_items_to_inventory
##############################

add_items_data = [
(0, ['iron'], {'level': 3, 'class': 'MAGE', 'inventory': {'wood': 10, 'iron': 4, 'feathers': 1, 'string': 2}, 'total_weight': 17.0}, 1),
(1, ['wood', 'wood', 'iron', 'sage', 'sand', 'clay', 'sand', 'clay', 'wood', 'iron'], {'level': 4, 'class': 'KNIGHT', 'inventory': {'wood': 6, 'iron': 3, 'stone': 5, 'sage': 1, 'sand': 2, 'clay': 2}, 'total_weight': 19.0}, 10),
(2, ['sand', 'iron', 'ivy', 'wood', 'water', 'clay', 'sage', 'water', 'iron'], {'level': 1, 'class': 'THIEF', 'inventory': {'wood': 4, 'iron': 3, 'sand': 1, 'ivy': 1, 'water': 2, 'clay': 1, 'sage': 1}, 'total_weight': 13.0}, 9),
(3, ['water', 'clay', 'leaf', 'water', 'iron', 'sage', 'string'], {'level': 6, 'class': 'THIEF', 'inventory': {'wood': 3, 'iron': 2, 'water': 2, 'clay': 1, 'leaf': 1, 'sage': 1, 'string': 1}, 'total_weight': 11.0}, 7),
(4, [], {'level': 0, 'class': 'THIEF', 'inventory': {'wood': 10}, 'total_weight': 10.0}, 0)
]


@pytest.mark.parametrize("ix, items, expected_player, expected_added", add_items_data)
def test_add_items_to_inventory(ix, items, expected_player, expected_added):
    """ Test code for add_items_to_inventory """
    steps = basic_steps + [ "players = load_players()",
            f"player = players[{ix}]",
            f"items = {items}",
            "hw6.add_items_to_inventory(player, items)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    player_copy = copy.deepcopy(players[ix])

    try:
        actual = hw6.add_items_to_inventory(player_copy, items)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected_added)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_result(player_copy, expected_player)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


###############################
# Tests for all_craftable_items
###############################

all_craftable_data = [
    (0,[{'name': 'staff', 'level': 3, 'class': 'MAGE', 'materials': {'wood': 2, 'string': 1}, 'power': 4}]),
(1,[{'name': 'shield', 'level': 4, 'class': 'KNIGHT', 'materials': {'wood': 3}, 'power': 20}]),
(2,[]),
(3,[{'name': 'axe', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 3, 'iron': 1}, 'power': 5}, {'name': 'plank', 'level': 2, 'class': 'THIEF', 'materials': {'wood': 2}, 'power': 5}])
]

@pytest.mark.parametrize("ix, expected", all_craftable_data)
def test_all_craftable_items(ix, expected):
    """ Test code for all_craftable_items """
    steps = basic_steps + [ "players = load_players()",
                           "crafting_recipes = load_recipes()",
            f"player = players[{ix}]",
            "hw6.all_craftable_items(crafting_recipes, player)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw6.all_craftable_items(crafting_recipes, players[ix])
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


###############################
# Tests for craft_max_power
###############################

craft_max_power_data = [
(0,{'level': 3, 'class': 'MAGE', 'inventory': {'wood': 8, 'iron': 3, 'feathers': 1, 'string': 1, 'staff': 1}, 'total_weight': 14.0}, 4),
(1,{'level': 4, 'class': 'KNIGHT', 'inventory': {'iron': 1, 'stone': 5, 'shield': 1}, 'total_weight': 7.0}, 20),
(2,{'level': 1, 'class': 'THIEF', 'inventory': {'wood': 3, 'iron': 1}}, 0),
(3,{'level': 6, 'class': 'THIEF', 'inventory': {'axe': 1}, 'total_weight': 1.0}, 5),
(4,{'level': 0, 'class': 'THIEF', 'inventory': {'wood': 10}}, 0),
]

@pytest.mark.parametrize("ix, expected_player, expected_power", craft_max_power_data)
def test_craft_max_power(ix, expected_player, expected_power):
    """ Test code for craft_max_power """
    steps = basic_steps + [ "players = load_players()",
                           "crafting_recipes = load_recipes()",
            f"player = player[{ix}]",
            "hw6.craft_max_power(crafting_recipes, player)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    player_copy = copy.deepcopy(players[ix])

    try:
        actual = hw6.craft_max_power(crafting_recipes, player_copy)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected_power)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_result(player_copy, expected_player)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
    

