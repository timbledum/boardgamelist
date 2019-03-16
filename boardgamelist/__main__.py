"""Boardgamelist

A static website that showcases your board game collection.
"""

import click


@click.group()
def cli():
    pass


@cli.command()
def maintain():
    """Add or remove board games from the collection."""
    click.echo("Maintain")


@cli.command()
def update():
    """Download or update the board game data from BoardGameGeek."""
    click.echo("update")


@cli.command()
def build():
    """Build the static website from the board game data."""
    click.echo("build")


if __name__ == "__main__":
    cli()
