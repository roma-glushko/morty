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
    # click.echo(f"Hello {name}!")
    console = Console()

    table = Table(show_header=True, header_style="bold")

    table.add_column("created_at", style="dim", width=20)
    table.add_column("experiment_id")
    table.add_column("branch")

    experiments = ExperimentManager().get_all_experiments()

    for experiment in experiments:
        meta = experiment.get_meta()
        git = experiment.get_git_details()

        table.add_row(
            meta.created_at.strftime("%d %b, %y %H:%M:%S"),
            meta.experiment_id,
            git.current_branch,
        )

    console.print(table)


main = click.CommandCollection(sources=[leaderboard])

__all__ = ("main",)
