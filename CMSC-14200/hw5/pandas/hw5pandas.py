"""
HW5 pandas exercises (Task3).
***!!!used this link to help with panda function stuff:
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html
"""

import sys
import pandas as pd

cities = pd.read_csv("data_nba/cities.csv")
players = pd.read_csv("data_nba/players.csv")
teams = pd.read_csv("data_nba/teams.csv")
divisions = pd.read_csv("data_nba/divisions.csv")
games = pd.read_csv("data_nba/games.csv")
box = pd.read_csv("data_nba/box.csv")

def players_by_name_fragment(fragment: str) -> pd.DataFrame:
    """
    Return a DataFrame containing columns 'personId' and 'personName'.

    All players whose name contains the given fragment, case
    insensitive, must appear in the result.
    """
    player_names = players["personName"].str.contains(fragment, case = False)
    return players.loc[player_names, ["personId", "personName"]]

def ppg_by_name(name: str) -> float:
    """
    PPG stands for "points per game."

    Return the points per game for the given player whose name is
    exactly the given string, case sensitive. Please note that every
    player name in the data set is unique, so you need not worry
    about accidentally combining data from multiple players.

    Raise a ValueError if there is no such player.
    """
    player_data = players[players["personName"] == name]
    if player_data.empty:
        raise ValueError("Please enter valid player")

    player_id = player_data.iloc[0]["personId"]
    player_stats = box[box["personId"] == player_id]

    if player_stats.empty:
        return 0.0
    
    points = player_stats["points"].sum()
    games = player_stats["gameId"].nunique()
    return points / games

def played_for(team: str) -> pd.DataFrame:
    """
    Return a DataFrame containing columns 'personId' and
    'personName'. The result must contain no duplicate rows.

    The argument 'team' is a string like 'CHI' or 'MIN'.

    Raise a ValueError if the team does not exist.
    """
    if team not in teams["teamTricode"].unique():
        raise ValueError("Invalid Team Code")
    
    player_ids = box[box["teamTricode"] == team]["personId"]
    final = players[players["personId"].isin(player_ids)]
    return final[["personId", "personName"]]

def top_n_scorers_by_team(team: str, n: int) -> pd.DataFrame:
    """
    Return a DataFrame containing columns 'personId',
    'personName', and 'ppg'.

    Return the top n scorers for the given team by ppg. If n exceeds
    the number of scorers for that team, return as many as there are.

    Raise a ValueError if the team does not exist of if n<1.
    """
    if team not in teams["teamTricode"].unique():
        raise ValueError("Invalid Team Code")
    if n < 1:
        raise ValueError("n must be 1 or greater")
    
    team_box = box[box["teamTricode"] == team]
    if team_box.empty:
        return pd.DataFrame(["personId", "personName", "ppg"])
    
    points = team_box.groupby("personId")["points"].sum()
    games = team_box.groupby("personId")["gameId"].nunique()
    ppg = (points / games).reset_index(name = "ppg")

    added_ppg = ppg.merge(players[["personId", "personName"]])
    return added_ppg.sort_values("ppg", ascending = False).head(n)

def played_on_both(team1: str, team2: str) -> set[str]:
    """
    Return a set of strings, where each string is a player's name, for
    all players who have played on both team1 and team2.

    Raise a ValueError if either team does not exist.
    """
    if team1 not in teams["teamTricode"].unique() and \
    team2 not in teams["teamTricode"].unique():
        raise ValueError("Invalid Team Code(s)")
    
    team1_id = set(box[box["teamTricode"] == team1]["personId"])
    team2_id = set(box[box["teamTricode"] == team2]["personId"])
    shared_ids = team1_id & team2_id

    return set(players[players["personId"].isin(shared_ids)]["personName"])

def top_n_scorers_by_division(division: str, n: int) -> pd.DataFrame:
    """
    Return a DataFrame containing columns 'personId',
    'personName', and 'ppg'.

    Return the top n scorers for the given division by ppg. If n exceeds
    the number of scorers for that division, return as many as there are.

    Raise a ValueError if the division does not exist or if n<1.
    """
    if division not in divisions["division"].unique():
        raise ValueError("Invalid division")
    if n < 1:
        raise ValueError("n must be at least 1")
    
    teams_in_division = divisions[divisions["division"] == division]["teamTricode"]
    division_stats = box[box["teamTricode"].isin(teams_in_division)]

    points = division_stats.groupby("personId")["points"].sum()
    games = division_stats.groupby("personId")["gameId"].nunique()
    ppg = (points / games).reset_index(name = "ppg")

    return ppg.merge(players[["personId", "personName"]]).sort_values(by = "ppg", ascending = False).head(n)

def played_on_date(date: str) -> set[str]:
    """
    Return a set of player names for players who played on given
    date according to the data set.

    The date format is a YYYY-MM-DD string like '2024-02-03' (which is
    what is in the given CSV files).

    Answering this question requires inspecting the contents of games, box, and
    players, all three -- a Pandas 'merge' is recommended.

    It is not necessary to test that the date is in a particular span
    of time or that it is well-formatted; the function caller is
    responsible for supplying a reasonable date.

    """
    games_on_day = games[games["game_date"] == date]
    if games_on_day.empty:
        return set()
    
    game_id = games_on_day["gameId"]
    players_that_day = box[box["gameId"].isin(game_id)]["personId"].unique()

    return set(players[players["personId"].isin(players_that_day)]["personName"])
