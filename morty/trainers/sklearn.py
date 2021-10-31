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


class SklearnTrainingTracker(Callback):
    def __init__(self, experiment: Experiment):
        super().__init__()

        self.experiment = experiment

    def on_epoch_end(self, epoch, logs=None):  # pylint:disable=unused-argument
        # todo: implement metric logging
        pass
