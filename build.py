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

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import petl
from utils import get_html


env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html", "xml"])
)

data = petl.fromjson(INPUT)
data_formatted = data.format("weight", "{:.1f}").format(
    "image", '<img src="{}" alt="Board game image" height="200" width="200">'
)

html = get_html(data_formatted)
template = env.get_template("page.html")
html_output = template.render(table=html)

Path("output/page.html").write_text(html_output)
