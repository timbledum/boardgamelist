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

INPUT = "games.json"

from pathlib import Path
import json
from jinja2 import Environment, FileSystemBytecodeCache, select_autoescape
import petl
from utils import get_html


env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

with open(INPUT) as file:
    data = petl.fromjson(json.load(file))

html = get_html(data)
template = env.get_template("page.html")
html_output = template.render(table=html)

Path("output/page.html").write_text(html_output)