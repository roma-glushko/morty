import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from morty.experiments import Experiment


class BaseTracker(abc.ABC):
    """
    Interface of information trackers
    """

    def __init__(self, experiment: "Experiment"):
        self.experiment = experiment

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
