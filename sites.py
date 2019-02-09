"""Module for providing the constructors for the various sites."""

from collections import namedtuple

Page = namedtuple("Page", "file name function")
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
