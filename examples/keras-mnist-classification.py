import sys

sys.path.append("../..")  # noqa
sys.path.append("../../morty")  # noqa

import numpy as np  # noqa
from tensorflow import keras  # noqa
from tensorflow.keras import layers  # noqa

from morty.config import ConfigManager, config  # noqa
from morty.experiment import Experiment, ExperimentManager  # noqa
from morty.experiment.trainers.tensorflow import TrainingTracker  # noqa


@config(path="configs", name="basic_config")
def train(configs: ConfigManager) -> None:
    experiment: Experiment = ExperimentManager(configs=configs).create()

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    print(f"x_train shape: {x_train.shape}")
    print(f"{x_train.shape[0]} train samples")
    print(f"{x_test.shape[0]} test samples")

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, configs.num_classes)
    y_test = keras.utils.to_categorical(y_test, configs.num_classes)

    model = keras.Sequential(
        [
            keras.Input(shape=configs.image_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(configs.num_classes, activation="softmax"),
        ]
    )

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"],
    )

    model.summary()

    training_history = model.fit(
        x_train,
        y_train,
        epochs=configs.epochs,
        batch_size=configs.batch_size,
        validation_split=configs.val_dataset_fraction,
        callbacks=[TrainingTracker(experiment)],
    )

    experiment.log_artifact("training_history.pkl", training_history)

    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

    print(f"Test loss: {test_loss}")
    print(f"Test accuracy: {test_accuracy}")


if __name__ == "__main__":
    train()
