import click
from rich.console import Console

from morty.experiment.leaderboard.backend import create_backend_app


@click.group()
def leaderboard():
    pass


@leaderboard.command()
@click.option("--port", type=int, default=3007)
def open(port: int):
    """
    Opens morty's leaderboard
    """
    console = Console()

    # todo: fix reloading

    backend_app = create_backend_app()
    backend_app.run(port=port, debug=True)

    console.print("Opening a morty's board...")


main = click.CommandCollection(sources=(leaderboard,))

__all__ = ("main",)
