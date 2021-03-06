import os
import pickle
from datetime import datetime
from pathlib import Path

from funkybob import RandomNameGenerator
from typing import Optional, TypedDict, Any


class ExperimentContext(TypedDict):
    """
    Experiment context needed to resume existing experiment
    """
    id: str
    directory: str


class Experiment:
    """
    Experiment represents context of the current experiment
    with a set of methods to persist useful information
    """

    def __init__(self, root_directory: str, experiment_context: Optional[ExperimentContext] = None):
        self.root_directory: str = root_directory

        if experiment_context:
            # loading existing experiment
            self.experiment_id: str = experiment_context.id
            self.experiment_directory: str = experiment_context.directory

        if not experiment_context:
            # creating a new experiment
            self.experiment_id = self.generate_experiment_id()
            self.experiment_directory = self.experiment_id

    def get_directory(self) -> str:
        """
        Retrieve a path to the current experiment directory
        """
        return os.path.join(self.root_directory, self.experiment_directory)

    def get_file_path(self, file_name: str) -> str:
        """
        Retrieve a path to the current experiment directory
        """
        return os.path.join(self.root_directory, self.experiment_directory, file_name)

    def log_artifact(self, file_name: str, artifact: Any):
        """
        Log an object as a binary file
        """
        artifact_path: str = self.get_file_path(file_name)
        pickle.dump(artifact, open(artifact_path, 'wb'))

    def log_configs(self, configs: Any, file_ext: str = 'txt'):
        """
        Log configs as a text file
        """
        config_path: str = self.get_file_path('config.{}'.format(file_ext))
        pickle.dump(str(configs), open(config_path, 'wb'))

    def start(self):
        Path(self.get_directory()).mkdir(parents=True, exist_ok=True)

        # todo: run all standard trackers

    def finish(self):
        pass

    @staticmethod
    def generate_experiment_id() -> str:
        readable_id: str = next(iter(RandomNameGenerator()))
        timestamp: str = datetime.now().strftime('%Y%m%d_%H%M%S')

        return f'{timestamp}_{readable_id}'


class ExperimentManager:
    """
    ExperimentManager performs high level operations like experiment creation or loading
    """
    root_directory: str
    configs: Any

    def __init__(self, root_dir: str = 'experiments', configs: Optional[Any] = None):
        """

        """
        self.root_directory = root_dir
        self.configs = configs

    def create(self) -> Experiment:
        """
        Create a new experiment
        """
        experiment: Experiment = Experiment(self.root_directory)

        experiment.start()

        if self.configs:
            experiment.log_configs(self.configs)

        return experiment
