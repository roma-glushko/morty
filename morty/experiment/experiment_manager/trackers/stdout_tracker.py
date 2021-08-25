from morty.experiment.experiment_manager.experiment_manager import Experiment
from morty.experiment.experiment_manager.trackers.base import Tracker


class StdoutTracker(Tracker):
    """
    Track all script output to the separate file:
    - standard output
    - error output
    """

    def start(self, experiment: Experiment):
        pass

    def stop(self):
        pass
