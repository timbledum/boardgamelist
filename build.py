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

from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('yourapplication', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

