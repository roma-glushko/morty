from csv import DictReader
from datetime import datetime
from enum import Enum, unique
from glob import glob
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type

from funkybob import RandomNameGenerator
from pydantic import BaseModel

from morty.common import Directory, flatten_dict
from morty.dashboard.summarizers import summarize_trainings
from morty.trackers import BaseTracker
from morty.trackers.git import GitDetails


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
    train_run_summary = "train_run_summary.json"
    config = "config.txt"
    config_bin = "config.bin"
    git = "git.json"
    uncommitted_changes = "uncommitted_changes.diff"
    exceptions = "exceptions.log"
    stdout = "output.log"


class ExperimentMeta(BaseModel):
    created_at: datetime
    experiment_id: str
    train_runs: List[datetime] = []


class Experiment:
    """
    Experiment represents context of the current experiment
    with a set of methods to persist useful information
    """

    def __init__(
        self,
        root_directory: PathLike,
        existing_experiment_dir: Optional[PathLike] = None,
        experiment_trackers: Iterable[Type[BaseTracker]] = (),
    ):
        self.root_directory: Path = Path(root_directory)

        if existing_experiment_dir:
            self._load_experiment(existing_experiment_dir)
        else:
            self._init_new_experiment()

        self.experiment_trackers = experiment_trackers
        self.active_experiment_trackers: List[BaseTracker] = []

    def _init_new_experiment(self):
        self.created_at = datetime.now()
        self.experiment_id: str = generate_experiment_id()
        self.experiment_directory: Path = Path(
            generate_experiment_dir_name(self.created_at, self.experiment_id)
        )
        self.io = Directory(self.directory)
        self.train_run_io = Directory(self.train_run_directory)

    def _load_experiment(self, experiment_dir: PathLike):
        self.experiment_directory = Path(experiment_dir)
        self.io = Directory(self.directory)

        meta = self.meta

        self.created_at = meta.created_at
        self.experiment_id = meta.experiment_id

    @property
    def directory(self) -> Path:
        """
        Retrieve a path to the current experiment directory
        """
        return self.root_directory / self.experiment_directory

    @property
    def train_run_directory(self) -> Path:
        return self.directory / "train_runs"

    @property
    def train_runs(self) -> Iterable[DictReader]:
        return (
            DictReader(open(run_path, newline=""))
            for run_path in glob(
                str(self.train_run_directory / "*.csv"), recursive=True
            )
        )

    def log_configs(self, configs: dict):
        """
        Log configs as a text file
        """
        self.io.log_text(str(configs), "configs", file_ext="txt")

        try:
            self.io.log_json(flatten_dict(configs), filename="config", file_ext="json")
        except Exception as e:
            raise ValueError(
                f"Failed to serialize config object: \n "
                f"{str(e)} \n "
                f"Make sure it can be converted to a dictionary"
            )

    @property
    def configs(self) -> Dict[str, Any]:
        return self.io.get_json(filename="config")

    def log_exceptions(self, trace_lines: List[str]):
        """
        Log exceptions to a text file
        """
        self.io.log_text(trace_lines, "exceptions", file_ext="log")

    @property
    def exceptions(self) -> List[str]:
        return self.io.get_text(filename="exceptions", file_ext="log")

    def log_output(self, lines: Iterable[str]):
        """
        Log text as a std output or std error
        """
        self.io.log_text(lines, "output", file_ext="log")

    @property
    def output(self) -> List[str]:
        return self.io.get_text(filename="output", file_ext="log")

    def log_meta(self, meta: Optional[ExperimentMeta] = None):
        """
        Log Experiment Metadata
        """
        if not meta:
            meta = ExperimentMeta(
                experiment_id=self.experiment_id,
                created_at=self.created_at.timestamp(),
            )

        self.io.log_json(
            meta,
            filename="meta",
            file_ext="json",
        )

    @property
    def meta(self) -> ExperimentMeta:
        return ExperimentMeta(**self.io.get_json(filename="meta", file_ext="json"))

    def log_git_details(self, git_info: GitDetails):
        self.io.log_json(git_info, filename="git")

    @property
    def git(self) -> GitDetails:
        return GitDetails(**self.io.get_json(filename="git", file_ext="json"))

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

    def log_uncommitted_changes(self, uncommitted_changes: str):
        self.io.log_text(
            uncommitted_changes, filename="uncommitted_changes", file_ext="diff"
        )

    def log_train_run(self, experiment_created_at: datetime):
        meta: ExperimentMeta = self.meta

        meta.train_runs.append(experiment_created_at)

        self.log_meta(meta)

    def update_train_runs_summary(self):
        summary = summarize_trainings(self.train_runs)

        self.io.log_json(summary, "train_run_summary")
