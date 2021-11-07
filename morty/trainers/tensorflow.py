import csv
from datetime import datetime
from pathlib import Path
from typing import IO

from morty import Experiment

try:
    from tensorflow.keras.callbacks import Callback
except ImportError:
    try:
        from keras.callbacks import Callback
    except ImportError:
        msg = """
            You are trying to use TrainingTracker for Tensorflow/Keras.
            However, these libraries don't found. Please install them via:
            - pip install tensorflow
            - poetry add tensorflow"""
        raise ModuleNotFoundError(msg)


class TensorflowTrainingTracker(Callback):
    """
    Trainer Tracker for Tensorflow projects
    """

    def __init__(
        self,
        experiment: Experiment,
        log_file_template: str = "train_{:%Y%m%d_%H%M%S}.csv",
    ):
        super().__init__()

        self.experiment = experiment
        self.log_file_template = log_file_template

    def on_train_begin(self, logs=None):
        self.created_at: datetime = datetime.utcnow()
        self.log_file: str = self.log_file_template.format(self.created_at)
        self.log_path: Path = self.experiment.train_run_directory / self.log_file

        self.experiment.log_train_run(self.created_at)

        self.log_handle: IO = open(self.log_path, "w")
        self.writer = csv.writer(self.log_handle)

    def on_epoch_end(self, epoch, logs=None):
        # todo: handle a case when a new metric was added and the new output should be put
        # todo: to a new file

        if not self.log_path.stat().st_size:
            columns = ("epoch", *logs.keys())
            self.writer.writerow(columns)
            self.log_handle.flush()

        epoch_info = (epoch, *logs.values())

        self.writer.writerow(epoch_info)

    def on_train_end(self, logs=None):
        self.log_handle.close()

        self.experiment.update_train_runs_summary()

    def on_test_begin(self, logs=None):
        # todo: log test performance to test.csv file
        pass
