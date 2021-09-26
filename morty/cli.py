import click
from rich.console import Console
from rich.table import Table


@click.group()
def leaderboard():
    pass


@leaderboard.command()
def list():
    """
    Retrieves a list of experiments
    """
    # click.echo(f"Hello {name}!")
    console = Console()

    table = Table(show_header=True, header_style="bold")

    table.add_column("Date", style="dim", width=12)
    table.add_column("Title")
    table.add_column("Production Budget", justify="right")
    table.add_column("Box Office", justify="right")

    table.add_row(
        "Dev 20, 2019",
        "Star Wars: The Rise of Skywalker",
        "$275,000,000",
        "$375,126,118",
    )
    table.add_row(
        "May 25, 2018",
        "Solo: A Star Wars Story",
        "$275,000,000",
        "$393,151,347",
    )
    table.add_row(
        "Dec 15, 2017",
        "Star Wars Ep. VIII: The Last Jedi",
        "$262,000,000",
        "$1,332,539,889",
    )

    console.print(table)


main = click.CommandCollection(sources=[leaderboard])

__all__ = ("main",)
