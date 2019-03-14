"""Script for choosing and entering board games."""

from json import load, dump
import sys
import os.path


from boardgamegeek import BGGClient, BGGItemNotFoundError

from PyInquirer import prompt

FILE = "games.json"

MAIN_PROMPT = [
    {
        "type": "list",
        "name": "main_prompt",
        "message": "What would you like to do?",
        "choices": ["Enter new game", "Delete a game", "Quit"],
    }
]

GAME_PROMPT = [
    {
        "type": "input",
        "name": "game_prompt",
        "message": "Please enter the name of the game to search or (r) to return:",
        "validate": lambda x: True if x != "" else "Enter something!",
    }
]


def confirm_prompt(game_name):
    question = [
        {
            "type": "confirm",
            "name": "confirm_prompt",
            "message": f"Are you sure {game_name} is the correct game?",
            "default": True,
        }
    ]
    return question


def generate_game_questions(game_names):
    question = [
        {
            "type": "list",
            "name": "game",
            "message": "Which board game is it?",
            "choices": game_names + ["None - try again!"],
        }
    ]
    return question


def generate_games_to_delete(game_names):
    question = [
        {
            "type": "list",
            "name": "game",
            "message": "Which board game would you like to delete?",
            "choices": game_names + ["None - don't delete nothing!"],
        }
    ]
    return question


def ensure_file(file):
    if not os.path.isfile(file):
        with open(file) as json_file:
            dump([], json_file, indent=4)


def add_game(game):
    with open(FILE) as json_file:
        data = load(json_file)

    game_data = {"Game": game.name, "ID": game.id, "BGG name": game.name}
    data.append(game_data)

    with open(FILE, "w") as json_file:
        dump(data, json_file, indent=4)
    print("Game added!")


def new_game():
    client = BGGClient()
    not_found = True
    while not_found:

        game_search = prompt(GAME_PROMPT)["game_prompt"]
        if game_search.lower() == "r":
            return

        games = client.search(game_search)

        game_names = [game.name for game in games]
        if not game_names:
            print("No games found")
            continue

        game_questions = generate_game_questions(game_names)

        answer = prompt(game_questions)["game"]
        if answer == "None - try again!":
            continue
        if prompt(confirm_prompt(answer))["confirm_prompt"]:
            not_found = False

    add_game(games[game_names.index(answer)])


def delete_game():
    with open(FILE) as json_file:
        data = load(json_file)
    
    names = [game["BGG name"] for game in data]
    game_to_delete = prompt(generate_games_to_delete(sorted(names)))["game"]

    if game_to_delete != "None - don't delete nothing!":
        if prompt(confirm_prompt(game_to_delete))["confirm_prompt"]:
            index = names.index(game_to_delete)
            del data[index]
            with open(FILE, "w") as json_file:
                dump(data, json_file, indent=4)



def main():

    ensure_file(FILE)
    game_names = []

    cont = True
    while cont:
        answer = prompt(MAIN_PROMPT)
        if answer["main_prompt"] == "Quit":
            cont = False
        elif answer["main_prompt"] == "Enter new game":
            new_game()
        elif answer["main_prompt"] == "Delete a game":
            delete_game()


if __name__ == "__main__":
    main()
