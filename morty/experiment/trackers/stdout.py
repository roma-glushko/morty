from morty.experiment.trackers import BaseTracker


class StdoutTracker(BaseTracker):
    """
    Track all script output to the separate file:
    - standard output
    - error output
    """

    def start(self):
        pass

    def stop(self):
        pass
