"""Module for providing the constructors for the various sites."""

from collections import namedtuple
import petl

Page = namedtuple("Page", "file name function category", defaults=[False])
pages = []


def rank(table):
    columns_to_keep = ["Board Game Geek link", "Name", "BGG ranking", "Minutes to play"]
    table_sorted = table.sort("BGG ranking")
    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("rank.html", "Games by BGG rank", rank))


def weight(table):
    columns_to_keep = [
        "Board Game Geek link",
        "Name",
        "Weighting (difficulty / complexity)",
        "BGG ranking",
        "Minutes to play",
    ]
    table_sorted = table.sort("Weighting (difficulty / complexity)")
    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("weighting.html", "Games by weight", weight))


def weight(table):
    columns_to_keep = ["Board Game Geek link", "Name", "Minutes to play", "BGG ranking"]
    table_sorted = table.sort("Minutes to play")
    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("length.html", "Games by length", weight))



def categories(table):
    category_list = [
        #"Abstract Strategy",
        "Adventure",
        "American West",
        "Ancient",
        #"Animals",
        "Aviation / Flight",
        "Bluffing",
        "Card Game",
        "City Building",
        "Civilization",
        #"Comic Book / Strip",
        "Deduction",
        "Dice",
        "Economic",
        #"Electronic",
        "Exploration",
        "Fantasy",
        "Farming",
        "Fighting",
        "Game System",
        #"Humor",
        #"Maze",
        #"Medical",
        "Medieval",
        #"Miniatures",
        #"Movies / TV / Radio theme",
        #"Murder/Mystery",
        #"Mythology",
        "Negotiation",
        #"Novel-based",
        "Party Game",
        #"Political",
        #"Prehistoric",
        #"Print & Play",
        #"Racing",
        "Real-time",
        "Science Fiction",
        "Spies/Secret Agents",
        #"Territory Building",
        "Trains",
        #"Wargame",
        #"Word Game",
        "World War II",
    ]

    columns_to_keep = ["Board Game Geek link", "Name", "BGG ranking", "Minutes to play"]

    table_sorted = table.sort("BGG ranking")

    tables = []
    for cat in category_list:
        group_table = table_sorted.selectcontains("Categories", cat)
        table_cut = group_table.cut(columns_to_keep)

        header = f"{cat} games"
        group = dict(header=header, table=table_cut)
        tables.append(group)

    return tables


pages.append(Page("categories.html", "Games by category", categories, True))


def players(table):
    columns_to_keep = ["Board Game Geek link", "Name", "BGG ranking", "Minutes to play"]

    minimum_players = int(table.stats("Minimum players").min)
    maximum_players = int(table.stats("Maximum players").max)

    table_sorted = table.sort("BGG ranking")

    def create_filter(player_count):
        return lambda row: (row["Minimum players"] <= player_count) and (
            row["Maximum players"] >= player_count
        )

    tables = []
    for player_count in range(minimum_players, maximum_players + 1):
        group_table = table_sorted.select(create_filter(player_count))
        table_cut = group_table.cut(columns_to_keep)

        header = f"Games with {player_count} player{'' if player_count == 1 else 's'}"
        group = dict(header=header, table=table_cut)
        tables.append(group)

    return tables


pages.append(Page("players.html", "Games by number of players", players, True))




def year(table):
    columns_to_keep = ["Board Game Geek link", "Name", "Year published", "BGG Ranking", "Minutes to play"]
    table_sorted = table.sort("Year published")

    table_cut = table_sorted.cut(columns_to_keep)
    return table_cut


pages.append(Page("year.html", "Games by year", year))


def minimum_age(table):
    columns_to_keep = ["Board Game Geek link", "Name", "BGG ranking", "Minutes to play"]

    ages = sorted(set(table["Minimum age"]))

    table_sorted = table.sort("BGG ranking")

    tables = []
    for age in ages:
        group_table = table_sorted.selecteq("Minimum age", age)
        table_cut = group_table.cut(columns_to_keep)

        header = f"Games with the minimum recommended age of {age}"
        group = dict(header=header, table=table_cut)
        tables.append(group)

    return tables


pages.append(Page("minimum_age.html", "Games by minimum age", minimum_age, True))