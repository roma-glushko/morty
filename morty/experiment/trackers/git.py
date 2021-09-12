import warnings
from pathlib import Path

from pydantic import BaseModel

from morty.experiment.trackers.base import BaseTracker


class GitDetails(BaseModel):
    current_branch: str
    current_commit_hash: str


def get_repository(project_path: Path):
    try:
        import git

        return git.Repo(project_path, search_parent_directories=True)
    except ImportError:
        warnings.warn(
            """
        git package should installed to track repository information:
        - pip install GitPython
        - poetry add GitPython
        """
        )


def get_repository_information(project_path: Path) -> GitDetails:
    repository = get_repository(project_path=project_path)

    current_commit = repository.head.commit

    current_branch = ""

    try:
        current_branch = repository.active_branch.name
    except TypeError as e:
        if str(e.args[0]).startswith(
            "HEAD is a detached symbolic reference as it points to"
        ):
            current_branch = "Detached HEAD"

    return GitDetails(
        current_commit_hash=current_commit.hexsha,
        current_branch=current_branch,
    )


class GitTracker(BaseTracker):
    """
    Track project repository information:
    - current branch
    - current commit hash
    - save untracked changes as a patch
    """

    def start(self):
        repository_info = get_repository_information(__file__)

        self.experiment.log_json(repository_info.dict(), filename="git")
        # todo: logs uncommitted changes as a patch file

    def stop(self):
        pass