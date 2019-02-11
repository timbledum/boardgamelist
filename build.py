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

from distutils.dir_util import copy_tree
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import petl
from sites import pages
from utils import get_html, clear_directory

INPUT = "game_data.json"
IMAGE_TAG = '<img src="{}" alt="Board game image" height="150" width="150">'
BGG_LINK_TAG = '<a href="https://boardgamegeek.com/boardgame/{}/">{}</a>'
BGG_LINK_FORMULA = lambda row: BGG_LINK_TAG.format(row["id"], row["image"])

COLUMN_MAPPING = {
    "id": "",
    "name": "Name",
    "bgg_rank": "Ranking",
    "categories": "Categories",
    "min_players": "Minimum players",
    "max_players": "Maximum players",
    "playing_time": "Minutes to play",
    "year": "Year published",
    "min_age": "Minimum age",
    "image": "Image",
    "weight": "Weighting (difficulty / complexity)",
}


def process_data(table):
    """Do some data cleaning on JASON input.

    - Turns IDs into links and image links into image tags.
    - Shortens the weight to one decimal place.
    """
    data_weight_formatted = table.format("weight", "{:.1f}")
    data_image_formatted = data_weight_formatted.format("image", IMAGE_TAG)
    data_link_added = data_image_formatted.addfield(
        "Board Game Geek link", BGG_LINK_FORMULA
    )
    data_final = data_link_added.rename(COLUMN_MAPPING)
    return data_final


def process_page(page, data, pages, env):
    """Render a page (defined by sites.py) into an html file."""
    data_processed = page.function(data)
    template = env.get_template("page.html")
    html_output = template.render(
        data=data_processed, name=page.name, pages=pages, category=page.category
    )
    Path("output/{}".format(page.file)).write_text(html_output, encoding="utf-8")


def main():
    """Set up jinga2 enviroment, extract data and save down to html files."""
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["petl2html"] = get_html

    data = petl.fromjson(INPUT)
    data_processed = process_data(data)

    # Refresh the output directory
    Path("output/").mkdir(exist_ok=True)
    clear_directory("output/")

    # Save home page
    home_template = env.get_template("index.html")
    html_output = home_template.render(pages=pages)
    Path("output/index.html").write_text(html_output, encoding="utf-8")

    # Save data-driven pages
    for page in pages:
        process_page(page, data_processed, pages, env)

    copy_tree("static", "output")


if __name__ == "__main__":
    main()
