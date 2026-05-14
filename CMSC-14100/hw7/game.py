import hw7
from game_data import *

def example_game():
    # Create items
    sword = get_sword()
    ingot = get_ingot()
    wood = get_wood()
    gold = get_gold()

    # Create players
    mage = get_mage()
    warrior = get_warrior()
    warrior2 = get_warrior_2()

    # Give players some starting gold
    mage.pick_up_item(gold, 100)
    warrior.pick_up_item(gold, 100)
    warrior2.pick_up_item(gold, 100)

    # Warrior picks up items and crafts a sword
    warrior.pick_up_item(item=ingot, quantity=2)
    warrior.pick_up_item(item=wood, quantity=1)
    warrior.craft_item(item=sword)

    # Trade between players
    print(f"{warrior2.name} is trying to buy a sword from {warrior.name}")
    warrior2.buy_item("Sword", quantity=1, other_player=warrior)

    # Sell back the sword
    print(f"{warrior2.name} is trying to sell a sword to {warrior2.name}")
    warrior2.sell_item("Sword", quantity=1, other_player=warrior)


if __name__ == "__main__":
    example_game()
