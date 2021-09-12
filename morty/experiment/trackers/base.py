import abc

from morty.experiment import Experiment


class BaseTracker(abc.ABC):
    def __init__(self, experiment: Experiment):
        self.experiment = experiment

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
