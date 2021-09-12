import sys
import tempfile

from morty.experiment import ExperimentManager
from morty.experiment.trackers import TracebackTracker


def test__traceback_tracker__start():
    temp_root_dir = tempfile.mkdtemp()
    experiment = ExperimentManager(temp_root_dir).create()

    tracker = TracebackTracker(experiment)
    handler_id = tracker._uuid
    exception_manager = tracker.exception_manager

    tracker.start()

    assert sys.excepthook == exception_manager._handle_exception
    assert exception_manager._handlers[handler_id] == tracker._log_exceptions

    tracker.stop()