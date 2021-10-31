import atexit
from glob import glob
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Type, Union

from morty.common import Directory
from morty.config import ConfigManager, NotebookConfigManager
from morty.dashboard.indexers import reindex_experiments
from morty.experiments import Experiment
from morty.trackers import DEFAULT_TRACKER_LIST

if TYPE_CHECKING:
    from morty.trackers import BaseTracker

Configs = Union[Dict, ConfigManager, NotebookConfigManager]


class ExperimentManager:
    """
    Performs high level operations like experiment creation or loading
    """

    def __init__(
        self,
        root_dir: Union[str, PathLike] = "experiments",
        experiment_trackers: Iterable[Type["BaseTracker"]] = DEFAULT_TRACKER_LIST,
        configs: Optional[Configs] = None,
        backup_files: Iterable[str] = (),
    ):
        self.root_directory = root_dir
        self.experiment_trackers = experiment_trackers
        self.configs = configs
        self.backup_files = backup_files
        self.io = Directory(Path(root_dir))

    def create(self) -> Experiment:
        """
        Create a new experiment and start all experiment trackers
        """
        experiment: Experiment = Experiment(
            Path(self.root_directory),
            experiment_trackers=self.experiment_trackers,
        )

        experiment.start(
            configs=self.configs,
            backup_files=self.backup_files,
        )

        atexit.register(lambda: experiment.finish())

        return experiment

    def reindex(self):
        index = reindex_experiments(self)

        self.io.log_json(index.dict(), filename=".index")

    def __iter__(self) -> Iterable[Experiment]:
        """
        Retrieves a collection of all experiments
        """

        for experiment_dir in glob(f"{self.root_directory}/*/"):
            experiment_directory = Path(experiment_dir)

            yield Experiment(
                root_directory=Path(self.root_directory),
                existing_experiment_dir=Path(experiment_directory.name),
            )
