# Morty

[![DeepSource](https://deepsource.io/gh/roma-glushko/morty.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/roma-glushko/morty/?ref=repository-badge)

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

```python
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

from morty.config import main, ConfigManager
from morty.experiment.experiment_manager import ExperimentManager, Experiment
from morty.experiment.experiment_manager.tensorflow import TrainingTracker


@main(config_path='configs', config_name='basic_config')
def train(config: ConfigManager) -> None:
    experiment: Experiment = ExperimentManager(configs=config).create()

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Scale images to the [0, 1] range
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    print(f"x_train shape: {x_train.shape}")
    print(f"{x_train.shape[0]} train samples")
    print(f"{x_test.shape[0]} test samples")

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, config.num_classes)
    y_test = keras.utils.to_categorical(y_test, config.num_classes)

    model = keras.Sequential(
        [
            keras.Input(shape=config.image_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(config.num_classes, activation='softmax'),
        ]
    )

    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy'],
    )

    model.summary()

    training_history = model.fit(
        x_train, y_train,
        epochs=config.epochs,
        batch_size=config.batch_size,
        validation_split=config.val_dataset_fraction,
        callbacks=[
            TrainingTracker(experiment)
        ]
    )

    experiment.log_artifact('training_history.pkl', training_history)

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
  title =        {Morty - a lightweight experiment and configuration library for small ML/DL projects and Kaggling},
  howpublished = {Github},
  year =         {2021},
  url =          {https://github.com/roma-glushko/morty}
}
```

## Credentials

Made with ❤️ by Roman Glushko (c)