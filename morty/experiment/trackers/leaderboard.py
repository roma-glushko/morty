from morty.experiment import Experiment
from morty.experiment.trackers import Tracker


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
