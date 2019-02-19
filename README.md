# Static website generator for board game listings #

[The website itself!](https://timbledum.github.io)

## Instructions ##

1. Clone this repository
2. Install requirements (`pip install -r requirements.txt`)
3. Update the games.json file to include the IDs and names of the board games you wish to list. The BGG name field is not used.
4. Run `python3 extractor.py` to download the board game information from Board Game Geek. It stores it in `game_data.json`.
5. Run `python3 build.py` to build the website into the `output` folder.
6. The website is now ready to host somewhere!

## Website concept ##

- Static website
- Two JSON files
    - One with the board game IDs (input)
    - One with downloaded information from BBG (produced by extractor.py)
- A script that refreshes board game data from BBG
- A collection of pages that sort the games in different ways:
    - Ranking
    - Weight
    - Length (in categories)
    - Category / ranking
    - Number of players / ranking
    - Age
- A way to build the website (build.py)
- Publish to github pages (currently manual)
- A pleasing template (currently based on github)
- Must have categories and ranking
- Must have links to BBG

## Fields collected (sample) ##

- Name
- Ranking
- Weight
- Category
- List of number of players
- Length