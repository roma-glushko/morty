import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional, Type, Dict

from funkybob import RandomNameGenerator
from pydantic import BaseModel

from morty.experiment.trackers import BaseTracker


def generate_experiment_id() -> str:
    """
    Generates unique experiment ID
    """
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
        experiment_trackers: Iterable[Type[BaseTracker]] = (),
        experiment_context: Optional[ExperimentContext] = None,
    ):
        self.root_directory: Path = Path(root_directory)
        self.experiment_id: str = generate_experiment_id()
        self.experiment_directory: Path = Path(self.experiment_id)
        self.experiment_trackers = experiment_trackers
        self.active_experiment_trackers: List[BaseTracker] = []

        if not experiment_context:
            return

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

    def log_text(self, lines: Iterable[str], filename: str, file_ext: str = "txt"):
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        with open(output_path, "a") as output_file:
            output_file.writelines(lines)

    def log_configs(self, configs: Any, file_ext: str = "txt"):
        """
        Log configs as a text file
        """
        self.log_text(str(configs), "config", file_ext=file_ext)

    def log_exception(self, trace_lines: List[str], file_ext: str = "log"):
        """
        Log exceptions to a text file
        """
        self.log_text(trace_lines, "exceptions", file_ext=file_ext)

    def log_output(self, lines: Iterable[str], file_ext: str = "log"):
        self.log_text(lines, "output", file_ext=file_ext)

    def log_json(self, data: Dict, filename: str, file_ext: str = "json"):
        """
        Save data as JSON file
        """
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        json.dump(data, open(output_path, "w"), indent=4, sort_keys=True)

    def start(self):
        """
        Starts experiment tracking
        """
        self.get_directory().mkdir(parents=True, exist_ok=True)

        self.active_experiment_trackers = self._activate_trackers(
            self.experiment_trackers
        )

    def finish(self):
        """
        Stops experiment tracking
        """
        self._deactivate_trackers(self.active_experiment_trackers)

    def _activate_trackers(
        self, experiment_trackers: Iterable[Type[BaseTracker]]
    ) -> List[BaseTracker]:
        active_trackers: List[BaseTracker] = []

        for tracker_class in experiment_trackers:
            tracker = tracker_class(self)

            tracker.start()
            active_trackers.append(tracker)

        return active_trackers

    @staticmethod
    def _deactivate_trackers(active_trackers: List[BaseTracker]):
        for tracker in active_trackers:
            tracker.stop()