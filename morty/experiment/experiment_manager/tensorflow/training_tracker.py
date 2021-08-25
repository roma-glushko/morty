import csv
from pathlib import Path

from morty.experiment.experiment_manager.experiment_manager import Experiment

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


class TrainingTracker(Callback):
    def __init__(self, experiment: Experiment):
        super().__init__()

        self.experiment = experiment

    def on_epoch_end(self, epoch, logs=None):
        log_path: Path = self.experiment.get_directory() / "train.csv"

        if not log_path.exists():
            with open(log_path, "w") as log_file:
                writer = csv.writer(log_file)
                writer.writerow(["epoch"] + [*logs.keys()])

        with open(log_path, "a") as log_file:
            writer = csv.writer(log_file)
            writer.writerow([epoch] + [*logs.values()])
