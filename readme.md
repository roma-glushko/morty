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

from examples.configs.basic_config import Config
from morty import Experiment, ExperimentManager
from morty.cli import Option, run
from morty.trainers import TensorflowTrainingTracker


def train(
    config: Config = Option(default=Config, help="Experiment Configurations")
) -> None:
    experiment: Experiment = ExperimentManager(configs=config).create()

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    y_train = keras.utils.to_categorical(y_train, config.num_classes)
    y_test = keras.utils.to_categorical(y_test, config.num_classes)

    model = keras.Sequential(
        [
            keras.Input(shape=config.image_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(config.num_classes, activation="softmax"),
        ]
    )

    model.compile(
        loss="categorical_crossentropy",
        optimizer=config.optimizer,
        metrics=("accuracy",),
    )

    model.summary()

    training_history = model.fit(
        x_train,
        y_train,
        epochs=config.epochs,
        batch_size=config.batch_size,
        validation_split=config.val_dataset_fraction,
        callbacks=(TensorflowTrainingTracker(experiment),),
    )

    experiment.log_artifact("training_history.pkl", training_history)

    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

    print(f"Test loss: {test_loss}")
    print(f"Test accuracy: {test_accuracy}")


if __name__ == "__main__":
    run(train)
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

## Acknowledgment

- https://github.com/aimhubio/aim
- https://devblog.pytorchlightning.ai/introducing-lightningcli-v2-supercharge-your-training-c070d43c7dd6
- https://github.com/neptune-ai/neptune-client
- https://github.com/wandb/client/tree/master/wandb
- https://github.com/allegroai/clearml
- https://keepsake.ai/
- https://guild.ai/why-guild/
- https://metaflow.org/
- https://github.com/IDSIA/sacred

## Credentials

Made with ❤️ by Roman Glushko (c)