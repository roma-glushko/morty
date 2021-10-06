import click
from rich.console import Console
from rich.table import Table

from morty.experiment import ExperimentManager


@click.group()
def leaderboard():
    pass


@leaderboard.command()
def list():
    """
    Retrieves a list of experiments
    """
    console = Console()

    with console.status("[bold green]Loading the leaderboard..."):
        table = Table(show_header=True, header_style="bold")

        table.add_column("created_at", style="dim", width=20)
        table.add_column("experiment_id")
        table.add_column("branch")

        for experiment in ExperimentManager().get_all_experiments():
            meta = experiment.meta
            git = experiment.git_details

            table.add_row(
                meta.created_at.strftime("%d %b, %y %H:%M:%S"),
                meta.experiment_id,
                git.branch,
            )

    console.print(table)


main = click.CommandCollection(sources=(leaderboard,))

__all__ = ("main",)
