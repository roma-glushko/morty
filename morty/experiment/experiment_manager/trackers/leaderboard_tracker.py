from morty.experiment.experiment_manager.experiment_manager import Experiment
from morty.experiment.experiment_manager.trackers.base import Tracker


class LeaderboardTracker(Tracker):
    """
    Maintain a global table of the best experiments
    """
    def __init__(self, experiment: Experiment):
        self.experiment = experiment

    def start(self):
        pass

    def stop(self):
        pass
