"""Boardgamelist

A static website that showcases your board game collection.
"""

import click

from maintain import main as maintain_run
from extractor import main as update_run
from build import main as build_run


@click.group()
def cli():
    pass


@cli.command()
def maintain():
    """Add or remove board games from the collection."""
    maintain_run()


@cli.command()
def update():
    """Download or update the board game data from BoardGameGeek."""
    update_run()


@cli.command()
def build():
    """Build the static website from the board game data."""
    build_run()


if __name__ == "__main__":
    cli()
