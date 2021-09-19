import atexit
from typing import TYPE_CHECKING, Any, Iterable, Optional, Type

from morty.experiment.experiments import Experiment
from morty.experiment.trackers import DEFAULT_TRACKER_LIST

if TYPE_CHECKING:
    from morty.experiment.trackers import BaseTracker


class ExperimentManager:
    """
    Performs high level operations like experiment creation or loading
    """

    def __init__(
        self,
        root_dir: str = "./experiments",
        experiment_trackers: Iterable[Type["BaseTracker"]] = DEFAULT_TRACKER_LIST,
        configs: Optional[Any] = None,
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
            self.root_directory,
            experiment_trackers=self.experiment_trackers,
        )

        experiment.start(
            configs=self.configs,
            backup_files=self.backup_files,
        )

        atexit.register(lambda: experiment.finish())

        return experiment

