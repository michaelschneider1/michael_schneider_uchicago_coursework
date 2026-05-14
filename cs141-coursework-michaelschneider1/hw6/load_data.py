"""
CMSC 14100
Updated Winter 2025

Data Loading Functions for Homework #6
"""

import json

def load_recipes():
    """
    Load crafting recipes from a JSON file.

    Returns:
        List[Dict[str,Any]]: a list of crafting recipes
    """
    with open("data/crafting_recipes.json", "r") as f:
        recipes = json.load(f)
    return recipes

def load_invalid_recipes():
    """
    Load invalid crafting recipes from a JSON file.

    Returns:
        List[Dict[str,Any]]: a list of invalid crafting recipes
    """
    with open("data/invalid_recipes.json", "r") as f:
        invalid_recipes = json.load(f)
    return invalid_recipes

def load_players():
    """
    Load player data from a JSON file.

    Returns:
        List[Dict[str,Any]]: a list of player data
    """
    with open("data/players.json", "r") as f:
        players = json.load(f)
    return players