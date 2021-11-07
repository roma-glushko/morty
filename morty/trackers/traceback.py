import sys
import threading
import uuid
from typing import TYPE_CHECKING, Callable, Dict, Iterable, List
from uuid import UUID

from morty.trackers import BaseTracker

if TYPE_CHECKING:
    from morty import Experiment

ExceptionHandler = Callable[[List[str]], None]


class ExceptionManager:
    """
    Registers and unregisters global exception handlers
    """

    def __init__(self, exception_handlers: Iterable[ExceptionHandler] = ()):
        self._previous_exception_manager = None
        self._lock = threading.Lock()
        self._handlers: Dict[UUID, ExceptionHandler] = {}

        self._handlers.update(
            {uuid.uuid4(): handler_func for handler_func in exception_handlers}
        )

    def activate(self):
        """
        Activates a custom global exception manager
        """
        with self._lock:
            self._previous_exception_manager = sys.excepthook
            sys.excepthook = self._handle_exception

    def deactivate(self):
        """
        Deactivates a custom global exception manager
        """
        with self._lock:
            sys.excepthook = self._previous_exception_manager
            self._previous_exception_manager = None

    def register(self, handler_id: UUID, handler_func: ExceptionHandler):
        """
        Register a custom exception handler with unique ID
        """
        with self._lock:
            self._handlers[handler_id] = handler_func

    def unregister(self, handler_id: UUID):
        """
        Remove a custom exception handler with specified ID
        """
        with self._lock:
            if handler_id not in self._handlers:
                return

            del self._handlers[handler_id]

    def _handle_exception(self, exception: List[str]):
        """
        High-level exception handling logic
        """
        for _, handler_func in self._handlers.items():
            handler_func(exception)


class TracebackTracker(BaseTracker):
    """
    Tracks unhandled exceptions and log them to experiment directory
    """

    def __init__(self, experiment: "Experiment"):
        super().__init__(experiment)

        self._uuid: UUID = uuid.uuid4()
        self.exception_manager: ExceptionManager = ExceptionManager()

    def start(self):
        """
        Log global exceptions to the experiment folder
        """

        self.exception_manager.register(self._uuid, self._log_exceptions)
        self.exception_manager.activate()

    def stop(self):
        """
        Remove all global exception handlers
        """
        self.exception_manager.unregister(self._uuid)
        self.exception_manager.deactivate()

    def _log_exceptions(self, trace_lines: List[str]):
        """
        Log critical exceptions
        """
        self.experiment.log_exceptions(trace_lines)
