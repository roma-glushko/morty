from typing import Tuple, Type

from morty.trackers.base import BaseTracker
from morty.trackers.git import GitTracker
from morty.trackers.stdout import StdoutTracker
from morty.trackers.traceback import TracebackTracker

DEFAULT_TRACKER_LIST: Tuple[Type[BaseTracker], ...] = (
    GitTracker,
    StdoutTracker,
    TracebackTracker,
)

__all__ = (
    "BaseTracker",
    "GitTracker",
    "StdoutTracker",
    "TracebackTracker",
    "DEFAULT_TRACKER_LIST",
)
