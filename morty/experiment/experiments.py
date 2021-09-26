import json
import pickle
from datetime import datetime
from enum import Enum, unique
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type

from funkybob import RandomNameGenerator

from morty.experiment.trackers import BaseTracker


def generate_experiment_id() -> str:
    """
    Generates unique experiment ID
    """
    return next(iter(RandomNameGenerator()))


def generate_experiment_dir_name(created_at: datetime, experiment_id: str) -> str:
    """
    Generates experiment directory name
    """
    return f"{created_at.strftime('%Y%m%d_%H%M%S')}_{experiment_id}"


@unique
class ExperimentFiles(str, Enum):
    meta = "meta.json"
    config = "config.txt"
    config_bin = "config.bin"
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
        existing_experiment_dir: Optional[str] = None,
        experiment_trackers: Iterable[Type[BaseTracker]] = (),
    ):
        self.root_directory: Path = Path(root_directory)

        if existing_experiment_dir:
            self._load_experiment(existing_experiment_dir)
        else:
            self._init_new_experiment()

        self.io = ExperimentIO(self.get_directory())

        self.experiment_trackers = experiment_trackers
        self.active_experiment_trackers: List[BaseTracker] = []

    def _init_new_experiment(self):
        self.created_at = datetime.now()
        self.experiment_id: str = generate_experiment_id()
        self.experiment_directory: Path = Path(
            generate_experiment_dir_name(self.created_at, self.experiment_id)
        )

    def _load_experiment(self, experiment_dir: str):
        self.experiment_directory = experiment_dir

        meta = self.get_meta()

        self.created_at = meta["created_at"]
        self.experiment_id = meta["experiment_id"]

    def get_directory(self) -> Path:
        """
        Retrieve a path to the current experiment directory
        """
        return self.root_directory / self.experiment_directory

    def log_configs(self, configs: Any):
        """
        Log configs as a text file
        """
        self.io.log_text(str(configs), "configs", file_ext="txt")
        self.io.log_binary("configs.bin", configs)

    def get_configs(self) -> List[str]:
        return self.io.get_text(filename="config", file_ext="log")

    def log_exceptions(self, trace_lines: List[str]):
        """
        Log exceptions to a text file
        """
        self.io.log_text(trace_lines, "exceptions", file_ext="log")

    def get_exceptions(self) -> List[str]:
        return self.io.get_text(filename="exceptions", file_ext="log")

    def log_output(self, lines: Iterable[str]):
        """
        Log text as a std output or std error
        """
        self.io.log_text(lines, "output", file_ext="log")

    def get_output(self) -> List[str]:
        return self.io.get_text(filename="output", file_ext="log")

    def log_meta(self):
        """
        Log Experiment Metadata
        """
        self.io.log_json(
            {
                "experiment_id": self.experiment_id,
                "created_at": self.created_at.timestamp(),
            },
            filename="meta",
            file_ext="json",
        )

    def get_meta(self):
        return self.io.get_json(filename="meta", file_ext="json")

    def log_artifact(self, file_name: str, artifact: Any):
        self.io.log_binary(file_name, artifact)

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

        self.log_meta()

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


class ExperimentIO:
    """
    Abstracts away all specific of working with filesystem
    """

    def __init__(self, experiment_dir: PathLike):
        self.experiment_dir = Path(experiment_dir)

    def get_file_path(self, file_name: str) -> Path:
        """
        Retrieve a path to the current experiment directory
        """
        return self.experiment_dir / file_name

    def log_binary(self, file_name: str, binary: Any):
        """
        Log an object as a binary file
        """
        binary_path: Path = self.get_file_path(file_name)
        pickle.dump(binary, open(binary_path, "wb"))

    def get_binary(self, file_name) -> Any:
        binary_path: Path = self.get_file_path(file_name)

        return pickle.load(open(binary_path, "rb"))

    def log_json(self, data: Dict, filename: str, file_ext: str = "json"):
        """
        Save data as JSON file
        """
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        json.dump(data, open(output_path, "w"), indent=4, sort_keys=True)

    def get_json(self, filename: str, file_ext: str = "json") -> Dict:
        file_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        return json.load(open(file_path, "r"))

    def log_text(self, lines: Iterable[str], filename: str, file_ext: str = "txt"):
        """
        Log strings as a plain text
        """
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        with open(output_path, "a") as output_file:
            output_file.writelines(lines)

    def get_text(self, filename: str, file_ext: str = "txt") -> List[str]:
        file_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        return open(file_path, "r").readlines()
