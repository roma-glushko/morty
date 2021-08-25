from pydantic import BaseModel

from morty.experiment.experiment_manager.experiment_manager import Experiment
from morty.experiment.experiment_manager.trackers.base import Tracker


class GitDetails(BaseModel):
    current_branch: str
    current_commit_hash: str


class GitTracker(Tracker):
    """
    Track project repository information:
    - current branch
    - current commit hash
    - save untracked changes as a patch
    """

    def start(self, experiment: Experiment):
        pass

    def stop(self):
        pass
