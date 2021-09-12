from morty.experiment.experiment_manager.experiment_manager import Experiment
from morty.experiment.experiment_manager.trackers.base import Tracker


class StdoutTracker(Tracker):
    """
    Track all script output to the separate file:
    - standard output
    - error output
    """
    def __init__(self, experiment: Experiment):
        self.experiment = experiment

    def start(self):
        pass

    def stop(self):
        pass
