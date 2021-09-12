from typing import Tuple, Type

from morty.experiment.trackers.base import BaseTracker
from morty.experiment.trackers.git import GitTracker
from morty.experiment.trackers.leaderboard import LeaderboardTracker
from morty.experiment.trackers.stdout import StdoutTracker
from morty.experiment.trackers.traceback import TracebackTracker

DEFAULT_TRACKER_LIST: Tuple[Type[BaseTracker], ...] = (
    GitTracker,
    StdoutTracker,
    TracebackTracker,
)

__all__ = (
    "LeaderboardTracker",
    "GitTracker",
    "StdoutTracker",
    "TracebackTracker",
    "DEFAULT_TRACKER_LIST",
)
