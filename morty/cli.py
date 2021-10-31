import contextlib
import os
import time
import webbrowser
from pathlib import Path

import click
from humanfriendly import format_timespan
from rich.console import Console

from morty.dashboard.backend import create_backend_app
from morty.managers import ExperimentManager


@contextlib.contextmanager
def timer(output: Console):
    start_time = time.time()
    yield
    output.print(
        f"✨ Done in {format_timespan(time.time() - start_time, detailed=True)}"
    )


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

    backend_app = create_backend_app()
    backend_app.run(port=port, debug=False)  # todo: fix reloading

    # TODO: open server in a separate thread
    console.print("Opening a morty's board...")
    webbrowser.open(f"http://localhost:{port}/")


@leaderboard.command()
@click.option("--root_dir", default=os.getcwd())
def index(root_dir: os.PathLike):
    """
    Opens morty's leaderboard
    """
    root_dir = Path(root_dir).resolve()
    console = Console()

    with timer(console):
        console.print(f"Indexing {root_dir}...")
        experiments = ExperimentManager(root_dir=root_dir)
        experiments.reindex()


main = click.CommandCollection(sources=[leaderboard])

__all__ = ("main",)
