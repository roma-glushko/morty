import abc

from morty.experiment.experiment_manager.experiment_manager import Experiment


class Tracker(abc.ABC):
    @abc.abstractmethod
    def start(self, experiment: Experiment):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
