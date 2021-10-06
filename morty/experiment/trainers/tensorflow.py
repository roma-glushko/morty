import csv
from pathlib import Path
from typing import IO

from morty.experiment import Experiment

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

    def __init__(self, experiment: Experiment, log_file="train.csv"):
        super().__init__()

        self.experiment = experiment
        self.log_file = log_file
        self.log_path: Path = self.experiment.get_directory() / self.log_file

    def on_train_begin(self, logs=None):
        self.log_handle: IO = open(self.log_path, "w")
        self.writer = csv.writer(self.log_handle)

    def on_epoch_end(self, epoch, logs=None):

        # todo: handle a case when a new metric was added and the new output should be put
        # todo: to a new file

        if not self.log_path.stat().st_size:
            columns = ("epoch", *logs.keys())
            self.writer.writerow(columns)

        epoch_info = (epoch, *logs.values())

        self.writer.writerow(epoch_info)

    def on_train_end(self, logs=None):
        # summarize train.csv file
        self.log_handle.close()
        pass

    def on_test_begin(self, logs=None):
        # todo: log test performance to test.csv file
        pass
