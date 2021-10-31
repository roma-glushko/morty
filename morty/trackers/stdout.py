import sys
from typing import TYPE_CHECKING, List, TextIO

from morty.trackers import BaseTracker

if TYPE_CHECKING:
    from morty.experiments import Experiment


class StreamLogger:
    """
    Decorates IO[str] class in order to log output
    """

    def __init__(self, experiment: "Experiment", stream: TextIO):
        self.experiment = experiment
        self.stream = stream

    def write(self, line: str) -> int:
        """
        Logs a string that is got to the stream
        """
        self.experiment.log_output([line])
        return self.stream.write(line)

    def writelines(self, lines: List[str]) -> None:
        """
        Logs all information that is got to the stream
        """
        self.experiment.log_output(lines)
        return self.stream.writelines(lines)

    def __getattr__(self, name):
        """
        Invokes methods that are not decorated
        """
        return getattr(self.stream, name)


class StdoutTracker(BaseTracker):
    """
    Track all script output to the separate file:
    - standard output
    - error output
    """

    def __init__(self, experiment: "Experiment"):
        super().__init__(experiment)

        self.stdout_logger = StreamLogger(experiment, sys.stdout)
        self.stderr_logger = StreamLogger(experiment, sys.stderr)

    def start(self):
        sys.stdout = self.stdout_logger
        sys.stderr = self.stderr_logger

    def stop(self):
        sys.stdout = self.stdout_logger.stream
        sys.stderr = self.stderr_logger.stream
