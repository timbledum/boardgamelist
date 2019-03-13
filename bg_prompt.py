"""Script for choosing and entering board games."""

from json import load, dump
import sys

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
        "validate": lambda x: True if x != "" else "Enter something!"
    }
]

def confirm_prompt(game_name):
    question = [
        {
            "type": "confirm",
            "name": "confirm_prompt",
            "message": f"Are you sure {game_name} is the correct game?",
            "default": True
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


def add_game(game):
    data = json.load(FILE)
    game_data =     {
        "Game": game.name,
        "ID": game.id
        "BBG name": game.name
    }
    data.append(game_data)
    json.dump(data, FILE, indent=4)
    print("Game added!")

def new_game():
    client = BGGClient()
    not_found = True
    while not_found:

        game_search = prompt(GAME_PROMPT)["game_prompt"]
        print(game_search)
        if game_search.lower() == "r":
            return

        games = client.search(game_search)
        print(games)

        game_names = [game.name for game in games]

        game_questions = generate_game_questions(game_names)

        answer = prompt(game_questions)['game']
        if answer == "None - try again!":
            continue
        if prompt(confirm_prompt(answer))["confirm_prompt"]:
            not_found = False

    add_game(games[game_names.index(answer)])


def delete_game():
    print("delete")


def main():

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
