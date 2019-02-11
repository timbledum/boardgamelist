"""Module for providing the constructors for the various sites."""

from collections import namedtuple
import petl

Page = namedtuple("Page", "file name function category", defaults=[False])
pages = []


def rank(table):
    columns_to_keep = ["Board Game Geek link", "Name", "Ranking", "Minutes to play"]
    table_sorted = table.sort("Ranking")
    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("index.html", "Games by rank", rank))


def weight(table):
    columns_to_keep = [
        "Board Game Geek link",
        "Name",
        "Weighting (difficulty / complexity)",
        "Ranking",
        "Minutes to play",
    ]
    table_sorted = table.sort("Weighting (difficulty / complexity)")
    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("weighting.html", "Games by weight", weight))


def weight(table):
    columns_to_keep = ["Board Game Geek link", "Name", "Minutes to play", "Ranking"]
    table_sorted = table.sort("Minutes to play")
    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("length.html", "Games by length", weight))


def players(table):
    columns_to_keep = ["Board Game Geek link", "Name", "Ranking", "Minutes to play"]

    minimum_players = int(table.stats('Minimum players').min)
    maximum_players = int(table.stats('Maximum players').max)

    table_sorted = table.sort("Ranking")

    def create_filter(player_count):
        return lambda row: (row["Minimum players"] <= player_count) and (row["Maximum players"] >= player_count)

    tables = []
    for player_count in range(minimum_players, maximum_players + 1):
        group_table = table_sorted.select(create_filter(player_count))
        table_cut = group_table.cut(columns_to_keep)

        header = f"Games with {player_count} player{'' if player_count == 1 else 's'}"
        group = dict(header=header, table=table_cut)
        tables.append(group)

    return tables


pages.append(Page("players.html", "Games by number of players", players, True))
