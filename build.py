"""Script for building the website.

In order, this script:

- Loads the JSON data
- Generates a petl table
- Does some data clean-up:
    - Turns numbers into well formatted text
    - Creates links from IDs
    - Creates image tags from image links
- Feeds the data into jinja2 to create the sites specified by sites
- Generates the files into the output directory
- [Optional extra] - deploy to github if the right tag is present

"""

INPUT = "game_data.json"
IMAGE_TAG = '<img src="{}" alt="Board game image" height="200" width="200">'
BGG_LINK_TAG = '<a href="https://boardgamegeek.com/boardgame/{}/">{}</a>'
BGG_LINK_FORMULA = lambda row: BGG_LINK_TAG.format(row["id"], row["image"])

COLUMN_MAPPING = {"id": "",
"name": "Name",
"bgg_rank": "Ranking",
"categories": "Categories",
"min_players": "Minimum players",
"max_players": "Maximum players",
"playing_time": "Minutes to play",
"year": "Year published",
"min_age": "Minimum age",
"image": "Image",
"weight": "Weighting (difficulty / complexity)",}

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import petl
from sites import pages
from utils import get_html


env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html", "xml"])
)

data = petl.fromjson(INPUT)
data_weight_formatted = data.format("weight", "{:.1f}")
data_image_formatted = data_weight_formatted.format("image", IMAGE_TAG)
data_link_added = data_image_formatted.addfield("Board Game Geek link", BGG_LINK_FORMULA)
data_final = data_link_added.rename(COLUMN_MAPPING)

def process_page(page, data):
    data_processed = page.function(data)
    html = get_html(data_processed)
    template = env.get_template("page.html")
    html_output = template.render(table=html, name=page.name)
    Path("output/{}".format(page.file)).write_text(html_output)

for page in pages:
    process_page(page, data_final)
