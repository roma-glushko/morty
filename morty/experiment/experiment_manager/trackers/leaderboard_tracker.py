from morty.experiment.experiment_manager.experiment_manager import Experiment
from morty.experiment.experiment_manager.trackers.base import Tracker


class LeaderboardTracker(Tracker):
    """
    Maintain a global table of the best experiments
    """

    def start(self, experiment: Experiment):
        pass

    def stop(self):
        pass
