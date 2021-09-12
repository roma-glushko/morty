from morty.experiment import Experiment
from morty.experiment.trackers import Tracker


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
