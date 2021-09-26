import csv
from pathlib import Path

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

    def on_epoch_end(self, epoch, logs=None):
        log_path: Path = self.experiment.get_directory() / self.log_file

        # todo: handle a case when a new metric was added and the new output should be put
        # todo: to a new file

        if not log_path.exists():
            with open(log_path, "w") as log_file:
                writer = csv.writer(log_file)
                writer.writerow(["epoch"] + [*logs.keys()])

        epoch_info = [epoch] + [*logs.values()]

        with open(log_path, "a") as log_file:
            writer = csv.writer(log_file)
            writer.writerow(epoch_info)
