import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

from funkybob import RandomNameGenerator
from pydantic import BaseModel


def generate_experiment_id() -> str:
    readable_id: str = next(iter(RandomNameGenerator()))
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{timestamp}_{readable_id}"


class ExperimentContext(BaseModel):
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

    def __init__(
        self,
        root_directory: str,
        experiment_context: Optional[ExperimentContext] = None,
    ):
        self.root_directory: Path = Path(root_directory)
        self.experiment_id: str = generate_experiment_id()
        self.experiment_directory: Path = Path(self.experiment_id)

        if experiment_context:
            # loading existing experiment
            self.experiment_id = experiment_context.id
            self.experiment_directory = Path(experiment_context.directory)

    def get_directory(self) -> Path:
        """
        Retrieve a path to the current experiment directory
        """
        return self.root_directory / self.experiment_directory

    def get_file_path(self, file_name: str) -> Path:
        """
        Retrieve a path to the current experiment directory
        """
        return self.get_directory() / file_name

    def log_artifact(self, file_name: str, artifact: Any):
        """
        Log an object as a binary file
        """
        artifact_path: Path = self.get_file_path(file_name)
        pickle.dump(artifact, open(artifact_path, "wb"))

    def log_configs(self, configs: Any, file_ext: str = "txt"):
        """
        Log configs as a text file
        """
        config_path: Path = self.get_file_path("config.{}".format(file_ext))

        with open(config_path, "w") as config_file:
            config_file.writelines(str(configs))

    def log_exception(self, trace_lines: List[str]):
        """
        Log exceptions to a text file
        """
        exceptions_path: Path = self.get_file_path("exceptions.log")

        with open(exceptions_path, "a") as exceptions_file:
            exceptions_file.writelines(trace_lines)

    def start(self):
        self.get_directory().mkdir(parents=True, exist_ok=True)

        # todo: run all standard trackers

    def finish(self):
        pass
