import atexit
from glob import glob
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Type, Union

from morty.config import ConfigManager, NotebookConfigManager
from morty.experiment.experiments import Experiment
from morty.experiment.trackers import DEFAULT_TRACKER_LIST

if TYPE_CHECKING:
    from morty.experiment.trackers import BaseTracker

Configs = Union[Dict, ConfigManager, NotebookConfigManager]


class ExperimentManager:
    """
    Performs high level operations like experiment creation or loading
    """

    def __init__(
        self,
        root_dir: str = "./experiments",
        experiment_trackers: Iterable[Type["BaseTracker"]] = DEFAULT_TRACKER_LIST,
        configs: Optional[Configs] = None,
        backup_files: Iterable[str] = (),
    ):
        self.root_directory = root_dir
        self.experiment_trackers = experiment_trackers
        self.configs = configs
        self.backup_files = backup_files

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

    def get_all_experiments(self) -> Iterable[Experiment]:
        """
        Retrieves a collection of all experiments
        """
        experiments = []

        for experiment_dir in glob(f"{self.root_directory}/*/"):
            experiment_directory = Path(experiment_dir)

            experiments.append(
                Experiment(
                    root_directory=Path(self.root_directory),
                    existing_experiment_dir=Path(experiment_directory.name),
                )
            )

        return experiments
