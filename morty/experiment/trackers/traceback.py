import sys
import threading
import uuid
from typing import Callable, List
from uuid import UUID

from morty.experiment.trackers import BaseTracker
from morty.experiment.trainers import Experiment

ExceptionHandler = Callable[[List[str]], None]


class ExceptionManager:
    """
    Registers and unregisters global exception handlers
    """

    def __init__(self):
        self.previous_exception_manager = None
        self.lock = threading.Lock()

    def activate(self):
        pass

    def deactivate(self):
        with self.lock:
            sys.excepthook = self.previous_exception_manager
            self.previous_exception_manager = None

    def register(self, id: UUID, handler: ExceptionHandler):
        pass

    def unregister(self, id: UUID):
        pass


class TracebackTracker(BaseTracker):
    """
    Tracks unhandled exceptions and log them to experiment directory
    """

    def __init__(self, experiment: Experiment):
        super().__init__(experiment)

        self.uuid: UUID = uuid.uuid4()
        self.exception_manager: ExceptionManager = ExceptionManager()

    def start(self):
        def log_exceptions(trace_lines: List[str]):
            self.experiment.log_exception(trace_lines)

        self.exception_manager.register(self.uuid, log_exceptions)

    def stop(self):
        self.exception_manager.unregister(self.uuid)
