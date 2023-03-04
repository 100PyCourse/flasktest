"""
Handles logic for the pubg page.
Handles requests, dfs and images.
"""

import os
import time
import requests
import pandas as pd
import plotly.express as px


PUBG_API_KEY = os.environ["PUBG_API_KEY"]
pd.options.display.float_format = "{:,.4f}".format
TIMEOUT = 3

headers = {
    "Authorization": f"Bearer {PUBG_API_KEY}",
    "Accept": "application/vnd.api+json",
}

stats_list = ["damageDealt", "kills", "assists", "headshotKills", "roundMostKills",
              "rideDistance", "top10s", "roundsPlayed", "wins"]


def get_player_id(name):
    """Takes a player's name (str), contacts pubg API and returns either the player_id (str),
     429 if too many requests or 404 for incorrect "name" value or 0 if other error.
     """
    response = requests.get(
        f"https://api.pubg.com/shards/steam/players?filter[playerNames]={name}",
        headers=headers,
        timeout=TIMEOUT,
    )
    # Successful
    if response.status_code == 200:
        json_response = response.json()
        player_id = json_response["data"][0]["id"]
        return player_id

    # Missing request params
    if response.status_code == 400:
        return 400
    # Cannot find data
    if response.status_code == 404:
        return 404
    # Too many requests
    if response.status_code == 429:
        return 429
    # Unexpected error
    return 0


def get_seasons():
    """
    Contacts pubg API and returns either the valid seasons (list),
    429 if too many requests or 404 for incorrect "name" value or 0 if other error.
    Valid means after region updates.
    """
    response = requests.get(
        "https://api.pubg.com/shards/steam/seasons",
        headers=headers,
        timeout=TIMEOUT,
    )

    # Successful
    if response.status_code == 200:
        json_response = response.json()
        all_seasons = [x["id"] for x in json_response["data"]]
        valid_seasons = [x for x in all_seasons if "pc-" in x][::-1]
        return valid_seasons

    # Missing request params
    if response.status_code == 400:
        return 400
    # Cannot find data
    if response.status_code == 404:
        return 404
    # Too many requests
    if response.status_code == 429:
        return 429
    # Unexpected error
    return 0


def get_all_season_stats(player_id, valid_seasons, game_mode):
    """
    Takes player_id(str), valid_seasons(list) and game_mode(str).
    Contacts pubg API and returns all valid season stats, 429 if too many requests,
    404 for incorrect "name" value or 0 if other error.
    Valid means after region updates.
    """
    assists = []
    damage = []
    kills = []
    headshots = []
    most_kills = []
    distance = []
    top10s = []
    games = []
    wins = []
    seasons = []
    checked = 0

    # Sleep in case of too many requests
    for season in valid_seasons:
        if checked in (7, 15):
            time.sleep(60)
        checked += 1
        response = requests.get(
            f"https://api.pubg.com/shards/steam/players/{player_id}/seasons/{season}?filter["
            f"gamepad]=false",
            headers=headers,
            timeout=TIMEOUT,
        )

        # Successful
        if response.status_code == 200:
            try:
                data_json = response.json()
                stats = data_json["data"]["attributes"]["gameModeStats"][game_mode]
            except KeyError:
                return 404

        # Missing request params
        elif response.status_code == 400:
            return 400
        # Cannot find data
        elif response.status_code == 404:
            return 404
        # Too many requests
        elif response.status_code == 429:
            return 429
        # Unexpected error
        else:
            return 0

        if stats["roundsPlayed"] > 4:
            assists.append(stats["assists"])
            damage.append(stats["damageDealt"])
            kills.append(stats["kills"])
            headshots.append(stats["headshotKills"])
            most_kills.append(stats["roundMostKills"])
            distance.append(stats["rideDistance"])
            top10s.append(stats["top10s"])
            games.append(stats["roundsPlayed"])
            wins.append(stats["wins"])
            seasons.append("s." + season.split(".")[-1].split("-")[-1])
            print(f"{season} added")
        else:
            print(f"{season} skipped")

        if len(games) == 6:
            return [assists, damage, kills, headshots, most_kills,
                    distance, top10s, games, wins, seasons]

    return [assists, damage, kills, headshots, most_kills,
            distance, top10s, games, wins, seasons]


def create_dataframe(player_stats, name, mode):
    """
    Takes player_stats(list), valid_seasons(list) and game_mode(str).
    Saves and returns player stats as a df to be used later to create graphs.
    """
    mode = mode.replace("-", "_")
    df_player = pd.DataFrame()

    df_player["Season"] = player_stats[9]
    df_player["Games"] = player_stats[7]

    df_player["Wins"] = player_stats[8]
    df_player["Wins_g"] = df_player.Wins / df_player.Games

    df_player["Top10s"] = player_stats[8]
    df_player["Top10s_g"] = df_player.Top10s / df_player.Games

    df_player["Damage"] = player_stats[1]
    df_player["Damage_g"] = df_player.Damage / df_player.Games

    df_player["Kills"] = player_stats[2]
    df_player["Kills_g"] = df_player.Kills / df_player.Games

    df_player["Headshots"] = player_stats[3]
    df_player["Headshots_g"] = df_player.Headshots / df_player.Games

    df_player["Assists"] = player_stats[0]
    df_player["Assists_g"] = df_player.Assists / df_player.Games

    df_player["Most_Kills"] = player_stats[4]
    df_player["Most_Kills_g"] = df_player.Assists / df_player.Games

    df_player["Distance"] = player_stats[5]
    df_player["Distance_g"] = df_player.Distance / df_player.Games

    df_player.to_csv(f"flasktest/static/data/api/pubg/df_{name}_{mode}.csv", index=False)

    return df_player


def create_kills_bar(dataframe, name, mode):
    """
    Takes a df, player name(str) and game mode(str).
    Saves a png of a bar chart from entered data.
    Returns image location to be rendered.
    """
    color = "rgb(20,27,37)"
    kills_bar = px.bar(
        data_frame=dataframe,
        x="Season",
        y="Kills_g",
        title=f"Kills per game vs season | {name} {mode}",
    )
    kills_bar.update_traces(
        marker_color=color,
        marker_line_width=None,
        opacity=None,
    )

    kills_bar.update_layout(
        xaxis_title="Season",
        yaxis_title="Kills per game",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "family": "Josefin Sans",
            "size": 17,
            "color": color,
        },
    )
    kills_bar.write_image("flasktest/static/images/api/pubg/current_kills.png", scale=2)
    return "../static/images/api/pubg/current_kills.png"


def create_damage_bar(dataframe, name, mode):
    """
    Takes a df, player name(str) and game mode(str).
    Saves a png of a bar chart from entered data.
    Returns image location to be rendered.
    """
    color = "rgb(20,27,37)"
    damage_bar = px.bar(
        data_frame=dataframe,
        x="Season",
        y="Damage_g",
        title=f"Damage per game vs season | {name} {mode}",
    )
    damage_bar.update_traces(
        marker_color=color,
        marker_line_width=None,
        opacity=None,
    )

    damage_bar.update_layout(
        xaxis_title="Season",
        yaxis_title="Damage per game",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "family": "Josefin Sans",
            "size": 17,
            "color": color,
        },
    )

    damage_bar.write_image("flasktest/static/images/api/pubg/current_damage.png", scale=2)
    return "../static/images/api/pubg/current_damage.png"


def create_distance_bar(dataframe, name, mode):
    """
    Takes a df, player name(str) and game mode(str).
    Saves a png of a bar chart from entered data.
    Returns image location to be rendered.
    """
    color = "rgb(20,27,37)"
    distance_bar = px.bar(
        data_frame=dataframe,
        x="Season",
        y="Distance_g",
        title=f"Distance per game vs season | {name} {mode}",
    )
    distance_bar.update_traces(
        marker_color=color,
        marker_line_width=None,
        opacity=None,
    )

    distance_bar.update_layout(
        xaxis_title="Season",
        yaxis_title="Distance per game",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "family": "Josefin Sans",
            "size": 17,
            "color": color,
        },
    )

    distance_bar.write_image("flasktest/static/images/api/pubg/current_distance.png", scale=2)

    return "../static/images/api/pubg/current_distance.png"
