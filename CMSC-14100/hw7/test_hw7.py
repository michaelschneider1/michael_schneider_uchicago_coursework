"""
CMSC 14100
Winter 2025

Test code for Homework #7
"""
import pytest
import helpers
import sys  
import os



# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position

MODULE = "hw7"

from game_data import *
from hw7 import Item, Inventory, Player

def same_object(actual_object, expected_object):
    """ Helper function to check if two objects have the same attributes 
    and same values for those attributes"""
    if actual_object is None:
        return ("The Expected an object, got None instead\n"
           f"  Expected: {expected_object}\n"
           f"  Actual: {actual_object}")
    attr1 = vars(actual_object)
    attr2 = vars(expected_object)
    if attr1 != attr2:
        return ("The actual and expected object attributes of the object do not match\n"
           f"  Expected: {attr2}\n"
           f"  Actual: {attr1}")
    
    for attr in dir(expected_object):
        if getattr(actual_object, attr) != getattr(expected_object, attr):
            return (f"The actual and expected value of the {attr} attribute of the object do not match\n"
                    f"  Expected: {getattr(expected_object, attr)}\n"
                    f"  Actual: {getattr(actual_object, attr)}")
    
    return None

def test_item_use():
    """ Test that that a sword can be used a finite amount of times before being broken"""
    item = get_sword()
    steps = [
        "from game data import get_sword",
        "sword = get_sword()"
    ]
    steps.extend(["sword.use()"]*5)

    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        for _ in range(4):
            err_msg = helpers.check_result(item.use(), True)
            if err_msg is not None:
                pytest.fail(err_msg + recreate_msg)
 
        err_msg = helpers.check_result(item.use(), False)

        if err_msg is not None:
            pytest.fail(err_msg + "\n\nNOTE: The Sword must break on the Fifth Use!" + recreate_msg)

        err_msg = helpers.check_result(item.use(), False)

        if err_msg is not None:
            pytest.fail(err_msg + "\n\nNOTE: The Sword must remain broken after the fifth use!" + recreate_msg +"\nsword.use()\n")

    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

def test_item_price():
    """ Test that the price of a sword drops after being broken """
    item = get_sword()
    steps = [
        "from game data import get_sword",
        "sword = get_sword()",
        "sword.price()"
    ]

    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:

        err_msg = helpers.check_result(item.price(), 50)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
        steps.extend(["sword.use()"]*5 + ["sword.price()"])
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

        for _ in range(5):
            item.use()
 
        err_msg = helpers.check_result(item.price(), 1)
        if err_msg is not None:
            pytest.fail(err_msg + "\n\nNOTE: The Sword should be priced at 1 after breaking!" + recreate_msg)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

@pytest.mark.parametrize("item_name, function, item, expected_qty", 
                          [
                              ("Sword", "get_sword", get_sword(), 1),
                              ("Gold", "get_gold", get_gold(), 50),
                              ("Wood", "get_wood", get_wood(), 100),
                              ("Iron Ingot", "get_ingot", get_ingot(), 25),
                          ])
def test_inventory_add_get_item(item_name, function, item, expected_qty):
    """Test a single add/get item scenario"""
    steps = [
        f"from game data import {function}",
        f"item = {function}()",
        f"inventory = Inventory()"
    ]

    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        inventory = Inventory()

        steps.extend([f"inventory.add_item(item, {expected_qty})"])
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

        err_msg = helpers.check_none(inventory.add_item(item, expected_qty), None)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
        steps.extend([f'inventory.get_item("{item_name}")'])
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

        actual_item, actual_qty = inventory.get_item(item_name)

        err_msg = helpers.check_none(actual_item, item)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = same_object(actual_item, item)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, expected_qty)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


def test_inventory_total_weight_empty():
    """ Test that an empty inventory weighs 0.0"""
    recreate_msg = helpers.gen_recreate_commands(MODULE, ["inventory = hw7.Inventory()"])
    inventory = Inventory()
    err_msg = helpers.check_equals(inventory.total_weight(), 0.0)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("inventory_contents, expected_weight", 
                          [
                            ([("sword", get_sword(), 1), ("gold", get_gold(), 50)], 30.0),
                            ([("sword", get_sword(), 1), ("ingot", get_ingot(), 10)], 25.0),
                            ([("gold", get_gold(), 1), ("wood", get_wood(), 10)], 10.5),
                          ])
def test_inventory_total_weight(inventory_contents, expected_weight):
    """ Check empty inventory weight """
    steps = [
        "from game_data import *",
        "inventory = hw7.Inventory()"
    ]

    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    inventory = Inventory()

    try:
        for item_name, item, qty in inventory_contents:
            steps.extend(
                [
                    f"{item_name} = get_{item_name}()",
                    f"inventory.add_item({item_name}, {qty})"
                ]
            )
            inventory.add_item(item, qty)
            
        steps.append("inventory.total_weight()")
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

        err_msg = helpers.check_equals(inventory.total_weight(), expected_weight)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


@pytest.mark.parametrize("inventory_contents, recipe_name, recipe, expected",
                         [
                            ([("ingot", get_ingot(), 2), ("wood", get_wood(), 1)], "sword_recipe", sword_recipe, True),
                            ([("ingot", get_ingot(), 1), ("wood", get_wood(), 2)], "sword_recipe", sword_recipe, False),
                            ([("gold", get_gold(), 500), ("wood", get_wood(), 2)], "sword_recipe", sword_recipe, False),
                         ])
def test_inventory_has_items(inventory_contents, recipe_name, recipe, expected):
    """ Check Inventory.has_items """
    steps = [
        "from game_data import *",
        "inventory = hw7.Inventory()"
    ]

    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    try:
        inventory = Inventory()
        for item_name, item, qty in inventory_contents:
            steps.extend(
                [
                    f"{item_name} = get_{item_name}()",
                    f"inventory.add_item({item_name}, {qty})"
                ]
            )
            inventory.add_item(item, qty)
            
        steps.append(f"inventory.has_items({recipe_name})")
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

        err_msg = helpers.check_equals(inventory.has_items(recipe), expected)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


@pytest.mark.parametrize("inventory_contents, recipe_name, recipe, expected_remaining",
                         [
                            ([("ingot", get_ingot(), 2), ("wood", get_wood(), 1)], "sword_recipe", sword_recipe, {"Iron Ingot": (None, None), "Wood": (None, None)}),
                         ])
def test_inventory_remove_items(inventory_contents, recipe_name, recipe, expected_remaining):
    """ Check Inventory.has_items """
    steps = [
        "from game_data import *",
        "inventory = hw7.Inventory()"
    ]

    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    try:
        inventory = Inventory()
        for item_name, item, qty in inventory_contents:
            steps.extend(
                [
                    f"{item_name} = get_{item_name}()",
                    f"inventory.add_item({item_name}, {qty})"
                ]
            )
            inventory.add_item(item, qty)
            
        steps.append(f"inventory.remove_items({recipe_name})")
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

        inventory.remove_items(recipe)

        for item_name, (exp_item, exp_qty) in expected_remaining.items():
            actual_item, actual_qty = inventory.get_item(item_name)
            if exp_item is None:
                assert actual_item is exp_item, "Item not removed properly!"
            else:
                err_msg = same_object(actual_item, exp_item)
                if err_msg is not None: 
                    pytest.fail(err_msg + recreate_msg)
            if exp_qty is None:
                assert actual_qty is exp_qty, "Item not removed properly!"
            else:
                err_msg = helpers.check_equals(actual_qty, exp_qty)
                if err_msg is not None:
                    pytest.fail(err_msg + recreate_msg)
            
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

@pytest.mark.parametrize("player_varname, player, item_name, item, qty, allowed",
        [
        ("warrior", get_warrior(), "Sword", get_sword(), 1, True),
        ("mage", get_mage(), "Sword", get_sword(), 1, False),
        ])
def test_player_pick_up_item(player_varname, player, item_name, item, qty, allowed):
    """ Test if a Player is allowed to pick up an Item """

    steps = [
        "from game_data import *",
        f"player = get_{player_varname}()",
        f"{item_name.lower()} = get_{item_name.lower()}()",
        f"player.pick_up_item({item_name}, {qty})"

    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual_allowed = player.pick_up_item(item, 1)
        err_msg = helpers.check_result(actual_allowed, allowed)
        
        if allowed:
            # Additional check to see if the item is in inventory
            actual_item, actual_qty = player.inventory.get_item(item_name)

            err_msg = same_object(actual_item, item)
            if err_msg is not None:
                pytest.fail(err_msg + recreate_msg)

            err_msg = helpers.check_result(actual_qty, qty)
            if err_msg is not None:
                pytest.fail(err_msg + recreate_msg)
    
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)



@pytest.mark.parametrize("player_varname, player, inventory_contents, item_name, item, qty, allowed",
        [
        ("warrior", get_warrior(), [("ingot", get_ingot(), 2), ("wood", get_wood(), 1)], "Sword", get_sword(), 1, True),
        ("mage", get_mage(), [("ingot", get_ingot(), 2), ("wood", get_wood(), 1)], "Sword", get_sword(), 1, False),
        ])
def test_player_craft_item(player_varname, player, inventory_contents, item_name, item, qty, allowed):
    """ Test if a Player can craft an Item """

    steps = [
        "from game_data import *",
        f"player = get_{player_varname}()",
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        for inv_name, inv_item, inv_qty in inventory_contents:
            steps.extend(
                [
                    f"{inv_name} = get_{inv_name}()",
                    f"player.pick_up_item({inv_name}, {inv_qty})"
                ]
            )
            player.pick_up_item(inv_item, inv_qty)

        steps.extend([f"item = get_{item_name.lower()}()", "player.craft_item(item)"])
        recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
        actual_allowed = player.craft_item(item)
        err_msg = helpers.check_result(actual_allowed, allowed)
        
        if allowed:
            # Additional check to see if the item is in inventory
            actual_item, actual_qty = player.inventory.get_item(item_name)

            err_msg = same_object(actual_item, item)
            if err_msg is not None:
                pytest.fail(err_msg + recreate_msg)

            err_msg = helpers.check_result(actual_qty, qty)
            if err_msg is not None:
                pytest.fail(err_msg + recreate_msg)
    
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)



def test_player_buy_item_1():
    """ Test One Buy Transaction between player1 and player2"""
    steps = [
        "from game_data import *",
        "player1 = get_warrior()",
        "player2 = get_warrior_2()",
        "gold = get_gold()",
        "sword = get_sword()",
        "player1.pick_up_item(gold, 100)",
        "player2.pick_up_item(sword, 1)",
        'player1.buy_item("Sword", 1, player2)'
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        player1 = get_warrior()
        player2 = get_warrior_2()
        gold = get_gold()
        sword = get_sword()
        player1.pick_up_item(gold, 100)
        player2.pick_up_item(sword, 1)
        actual = player1.buy_item("Sword", 1, player2)

        err_msg = helpers.check_result(actual, True)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        item, qty = player1.inventory.get_item("Sword")
        # Check if item transferred correctly
        actual_item, actual_qty = player1.inventory.get_item("Sword")

        err_msg = same_object(actual_item, sword)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, 1)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
        # Check that sword no longer with Player 2
        actual_item, actual_qty = player2.inventory.get_item("Sword")

        err_msg = helpers.check_none(actual_item, None)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        # Check the gold Player 1 has
        actual_item, actual_qty = player1.inventory.get_item(CURRENCY)

        err_msg = same_object(actual_item, gold)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, 50)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        # Check the gold Player 1 has
        actual_item, actual_qty = player2.inventory.get_item(CURRENCY)

        err_msg = same_object(actual_item, gold)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, 50)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

def test_player_buy_item_2():
    """ Test One Buy Transaction between player1 and player2"""
    steps = [
        "from game_data import *",
        "player1 = get_warrior()",
        "player2 = get_mage()",
        "gold = get_gold()",
        "sword = get_sword()",
        "player1.pick_up_item(gold, 100)",
        "player2.pick_up_item(sword, 1)",
        'player1.buy_item("Sword", 1, player2)'
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        player1 = get_warrior()
        player2 = get_mage()
        gold = get_gold()
        sword = get_sword()
        player2.pick_up_item(gold, 100)
        player1.pick_up_item(sword, 1)
        actual = player2.buy_item("Sword", 1, player1)

        err_msg = helpers.check_result(actual, False)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

def test_player_buy_item_3():
    """ Test One Buy Transaction between player1 and player2"""
    steps = [
        "from game_data import *",
        "player1 = get_warrior()",
        "player2 = get_mage()",
        "gold = get_gold()",
        "sword = get_sword()",
        "player1.pick_up_item(gold, 20)",
        "player2.pick_up_item(sword, 1)",
        'player1.buy_item("Sword", 1, player2)'
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        player1 = get_warrior()
        player2 = get_warrior_2()
        gold = get_gold()
        sword = get_sword()
        player2.pick_up_item(gold, 20)
        player1.pick_up_item(sword, 1)
        actual = player2.buy_item("Sword", 1, player1)

        err_msg = helpers.check_result(actual, False)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

def test_player_sell_item_1():
    """ Test One Sale Transaction between player1 and player2"""
    steps = [
        "from game_data import *",
        "player1 = get_warrior()",
        "player2 = get_warrior_2()",
        "gold = get_gold()",
        "sword = get_sword()",
        "player1.pick_up_item(gold, 100)",
        "player2.pick_up_item(sword, 1)",
        'player1.buy_item("Sword", 1, player2)'
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        player1 = get_warrior()
        player2 = get_warrior_2()
        gold = get_gold()
        sword = get_sword()
        player1.pick_up_item(gold, 100)
        player2.pick_up_item(sword, 1)
        player2.sell_item("Sword", 1, player1)

        item, qty = player1.inventory.get_item("Sword")
        # Check if item transferred correctly
        actual_item, actual_qty = player1.inventory.get_item("Sword")

        err_msg = same_object(actual_item, sword)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, 1)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
        # Check that sword no longer with Player 2
        actual_item, actual_qty = player2.inventory.get_item("Sword")

        err_msg = helpers.check_none(actual_item, None)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        # Check the gold Player 1 has
        actual_item, actual_qty = player1.inventory.get_item(CURRENCY)

        err_msg = same_object(actual_item, gold)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, 50)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        # Check the gold Player 1 has
        actual_item, actual_qty = player2.inventory.get_item(CURRENCY)

        err_msg = same_object(actual_item, gold)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)

        err_msg = helpers.check_result(actual_qty, 50)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

def test_player_sell_item_2():
    """ Test One Sell Transaction between player1 and player2"""
    steps = [
        "from game_data import *",
        "player1 = get_warrior()",
        "player2 = get_mage()",
        "gold = get_gold()",
        "sword = get_sword()",
        "player2.pick_up_item(gold, 100)",
        "player1.pick_up_item(sword, 1)",
        'player1.sell_item("Sword", 1, player2)'
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        player1 = get_warrior()
        player2 = get_mage()
        gold = get_gold()
        sword = get_sword()
        player2.pick_up_item(gold, 100)
        player1.pick_up_item(sword, 1)
        actual = player1.sell_item("Sword", 1, player2)

        err_msg = helpers.check_result(actual, False)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

def test_player_sell_item_3():
    """ Test One Sell Transaction between player1 and player2"""
    steps = [
        "from game_data import *",
        "player1 = get_warrior()",
        "player2 = get_mage()",
        "gold = get_gold()",
        "sword = get_sword()",
        "player1.pick_up_item(gold, 20)",
        "player2.pick_up_item(sword, 1)",
        'player2.sell_item("Sword", 1, player2)'
    ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        player1 = get_warrior()
        player2 = get_warrior_2()
        gold = get_gold()
        sword = get_sword()
        player2.pick_up_item(gold, 20)
        player1.pick_up_item(sword, 1)
        actual = player2.buy_item("Sword", 1, player1)

        err_msg = helpers.check_result(actual, False)
        if err_msg is not None:
            pytest.fail(err_msg + recreate_msg)
        
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)



if __name__ == "__main__":
    pytest.main()
