import json
import pickle
from datetime import datetime
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type

from funkybob import RandomNameGenerator

from morty.experiment.trackers import BaseTracker


def generate_experiment_id() -> str:
    """
    Generates unique experiment ID
    """
    readable_id: str = next(iter(RandomNameGenerator()))
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{timestamp}_{readable_id}"


@unique
class ExperimentFiles(str, Enum):
    config = "config.txt"
    git = "git.json"
    uncommitted_changes = "uncommitted_changes.diff"
    exceptions = "exceptions.log"
    stdout = "output.log"


class Experiment:
    """
    Experiment represents context of the current experiment
    with a set of methods to persist useful information
    """

    def __init__(
            self,
            root_directory: str,
            experiment_trackers: Iterable[Type[BaseTracker]] = (),
    ):
        self.root_directory: Path = Path(root_directory)
        self.experiment_id: str = generate_experiment_id()
        self.experiment_directory: Path = Path(self.experiment_id)
        self.experiment_trackers = experiment_trackers
        self.active_experiment_trackers: List[BaseTracker] = []

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
        """
        Log strings as a plain text
        """
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
        """
        Log text as a std output or std error
        """
        self.log_text(lines, "output", file_ext=file_ext)

    def log_json(self, data: Dict, filename: str, file_ext: str = "json"):
        """
        Save data as JSON file
        """
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        json.dump(data, open(output_path, "w"), indent=4, sort_keys=True)

    def backup_files(self, backup_files: Iterable[str]):
        """
        Backup list of files
        """
        pass

    def start(
            self,
            configs: Optional[Any] = None,
            backup_files: Iterable[str] = (),
    ):
        """
        Starts experiment tracking
        """
        self.get_directory().mkdir(parents=True, exist_ok=True)

        if configs:
            self.log_configs(configs)

        if backup_files:
            self.backup_files(backup_files)

        self.active_experiment_trackers = self._activate_trackers(
            self.experiment_trackers
        )

    def finish(self):
        """
        Stops experiment tracking
        """
        self._deactivate_trackers()

    def _activate_trackers(
            self, experiment_trackers: Iterable[Type[BaseTracker]]
    ) -> List[BaseTracker]:
        """
        Activates all trackers to log all kind of information about experiment
        """
        active_trackers: List[BaseTracker] = []

        for tracker_class in experiment_trackers:
            tracker = tracker_class(self)

            tracker.start()
            active_trackers.append(tracker)

        return active_trackers

    def _deactivate_trackers(self):
        """
        Stop active trackers when experiment is over
        """
        for tracker in self.active_experiment_trackers:
            tracker.stop()
