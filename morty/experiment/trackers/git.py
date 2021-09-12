import warnings
from pathlib import Path
from typing import Optional, Tuple

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


def get_repository_information(project_path: Path) -> Tuple[GitDetails, Optional[str]]:
    """
    Retrieve GIT repository information morty needs to log
    """
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

    uncommitted_changes = repository.git.diff('HEAD~1')

    return GitDetails(
        current_commit_hash=current_commit.hexsha,
        current_branch=current_branch,
    ), uncommitted_changes


class GitTracker(BaseTracker):
    """
    Track project repository information:
    - current branch
    - current commit hash
    - save untracked changes as a patch
    """

    def start(self):
        repo_info, uncommitted_changes = get_repository_information(__file__)

        self.experiment.log_json(repo_info.dict(), filename="git")

        if uncommitted_changes:
            self.experiment.log_text(uncommitted_changes, filename="uncommitted_changes", file_ext="diff")

    def stop(self):
        pass