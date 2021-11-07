# Morty

<img src="https://github.com/roma-glushko/morty/blob/master/img/morty-in-action.png?raw=true" width="600px" />

Morty is a lightweight experiment and configuration manager for small ML/DL projects and Kaggling.

Main Features:

- **Configuration Management**. Morty includes a config loading system based on the python files that makes you configure a wide variety of moving parts quickly and without overheads.
- **Experiment Management**. Morty provides a flexible, simple and local experiment management system that tracks a lots of context about your project state to make it possible to reproduce experiments.

## Installation

```bash
pip install morty
# or
poetry add morty
```

## Example of Usage

Trains a Keras model on MNIST:

```python
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

from morty.config import config, ConfigManager
from morty import ExperimentManager, Experiment
from morty.trainers import TensorflowTrainingTracker


@config(path="configs", name="basic_config")
def train(configs: ConfigManager) -> None:
    experiment: Experiment = ExperimentManager(configs=config).create()

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

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
        metrics=("accuracy",),
    )

    model.summary()

    training_history = model.fit(
        x_train, y_train,
        epochs=configs.epochs,
        batch_size=configs.batch_size,
        validation_split=configs.val_dataset_fraction,
        callbacks=(
            TensorflowTrainingTracker(experiment),
        )
    )

    experiment.log_artifact("training_history.pkl", training_history)

    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

    print(f"Test loss: {test_loss}")
    print(f"Test accuracy: {test_accuracy}")


if __name__ == "__main__":
    train()
```

## Citation

If Morty helped you to streamline your research, be sure to mention it via the following BibTeX entry:

```
@Misc{Glushko2021Morty,
  author =       {Roman Glushko},
  title =        {Morty - a lightweight experiment and configuration tracking library for small ML/DL projects and Kaggling},
  howpublished = {Github},
  year =         {2021},
  url =          {https://github.com/roma-glushko/morty}
}
```

## Credentials

Made with ❤️ by Roman Glushko (c)