"""Script for choosing and entering board games."""

from json import load, dump
import sys
from pathlib import Path



from boardgamegeek import BGGClient, BGGItemNotFoundError

from terminalprompts import list_prompt, confirmation_prompt, input_prompt

FILE = "games.json"
FOLDER = "game_data"
PATH = Path().parent / FOLDER / FILE

MAIN_MESSAGE = "What would you like to do?"
MAIN_CHOICES = ["Enter new game", "Delete a game", "Quit"]

GAME_MESSAGE = "Please enter the name of the game to search or (r) to return:"
GAME_CHOICE_MESSAGE = "Which board game is it?"
GAME_CANCEL_OPTION = "None - try again!"

DELETE_MESSAGE = "Which board game would you like to delete?"
DELETE_CANCEL_OPTION = "None - don't delete anything!"


def ensure_file(file):
    if not file.is_file():
        with open(file) as json_file:
            dump([], json_file, indent=4)


def add_game(game):
    with open(PATH) as json_file:
        data = load(json_file)

    game_data = {"Game": game.name, "ID": game.id, "BGG name": game.name}
    data.append(game_data)

    with open(PATH, "w") as json_file:
        dump(data, json_file, indent=4)
    print("Game added!")


def new_game():
    client = BGGClient()
    not_found = True
    while not_found:

        game_search = input_prompt(
            message=GAME_MESSAGE,
            validation_function=lambda x: True if x != "" else "Enter something!",
        )
        if game_search.lower() == "r":
            return

        games = client.search(game_search)

        game_names = [game.name for game in games]
        if not game_names:
            print("No games found")
            continue

        game_question_list = game_names + [GAME_CANCEL_OPTION]

        answer = list_prompt(message=GAME_CHOICE_MESSAGE, items=game_question_list)
        if answer == GAME_CANCEL_OPTION:
            continue
        if confirmation_prompt(message=f"Are you sure you would like to add {answer}?"):
            not_found = False

    add_game(games[game_names.index(answer)])


def delete_game():
    with open(PATH) as json_file:
        data = load(json_file)

    names = [game["BGG name"] for game in data]
    games_to_delete = sorted(names) + [DELETE_CANCEL_OPTION]
    game_to_delete = list_prompt(message=DELETE_MESSAGE, items=games_to_delete)

    if game_to_delete == DELETE_CANCEL_OPTION:
        return

    confirmation_message = f"Are you sure you would like to delete {game_to_delete}?"
    if not confirmation_prompt(message=confirmation_message):
        return

    index = names.index(game_to_delete)
    del data[index]
    with open(PATH, "w") as json_file:
        dump(data, json_file, indent=4)


def main():

    ensure_file(PATH)

    while True:
        answer = list_prompt(message=MAIN_MESSAGE, items=MAIN_CHOICES)
        if answer == "Quit":
            break
        elif answer == "Enter new game":
            new_game()
        elif answer == "Delete a game":
            delete_game()


if __name__ == "__main__":
    main()
