""" Module that extracts game details from board game geek via the API.

Loads and saves to JSON.

Assumes the ID of the game in the input file is under ID.

## Fields extracted ##
- Name
- Ranking
- Weight
- Category
- List of number of players
- Length
- Year
- Description
- Minimum age
- Image
"""

from json import load, dump
from boardgamegeek import BGGClient, BGGItemNotFoundError

INPUT = "games.json"
OUTPUT = "game_data.json"
FIELDS = [
    "ID",
    "name",
    "bgg_rank",
    "categories",
    "max_players",
    "min_players",
    "playing_time",
    "year" "description",
    "min_age",
    "image",
]


def search(game_id):
    """Return a game object from a game ID with some output and error checking."""
    client = BGGClient()

    print(f"Searching: {game_id}")
    try:
        return client.game(game_id=game_id)
    except BGGItemNotFoundError:
        print(f"{game_id} not found. :(")


def process_game(game):
    """Collect the relevant info from the game and return a dict."""

    game_dict = {field: getattr(game, field) for field in FIELDS}
    game_dict["weight"] = game.stats["averageweight"]
    return game_dict


def main():
    with open(INPUT) as file:
        games = load(file)

    games = [games[0]]
    print(games)

    game_objects = []
    for game in games:
        print(game)
        game_object = search(game["ID"])
        if game_object:
            game_objects.append(game_object)

    game_dicts = [process_game(game) for game in game_objects]

    dump(game_dicts, OUTPUT)


if __name__ == "__main__":
    main()
