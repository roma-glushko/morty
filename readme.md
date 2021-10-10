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

+---------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Train a Keras model on MNIST                                                          | Train a Keras model on MNIST with Morty                                               |
+---------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| .. code:: python                                                                      | .. code:: python                                                                      |
|                                                                                       |                                                                                       |
| import numpy as np                                                                    | import numpy as np                                                                    |
|                                                                                       |                                                                                       |
| from tensorflow import keras                                                          | from tensorflow import keras                                                          |
|                                                                                       |                                                                                       |
| from tensorflow.keras import layers                                                   | from tensorflow.keras import layers                                                   |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       | from morty.config import config, ConfigManager                                        |
| def train() -> None:                                                                  |                                                                                       |
|                                                                                       | from morty.experiment import ExperimentManager, Experiment                            |
|     # the data, split between train and test sets                                     |                                                                                       |
|                                                                                       | from morty.experiment.trainers import TensorflowTrainingTracker                       |
|     (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()           |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|     x_train, x_test = x_train.astype("float32") / 255, x_test.astype("float32") / 255 | @config(path="configs", name="basic_config")                                          |
|     x_train, x_test = np.expand_dims(x_train, -1), np.expand_dims(x_test, -1)         |                                                                                       |
|                                                                                       | def train(configs: ConfigManager) -> None:                                            |
|                                                                                       |                                                                                       |
|     y_train = keras.utils.to_categorical(y_train, configs.num_classes)                |     experiment: Experiment = ExperimentManager(configs=config).create()               |
|     y_test = keras.utils.to_categorical(y_test, configs.num_classes)                  |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |     (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()           |
|     model = keras.Sequential(                                                         |                                                                                       |
|                                                                                       |                                                                                       |
|         [                                                                             |     x_train, x_test = x_train.astype("float32") / 255, x_test.astype("float32") / 255 |
|                                                                                       |     x_train, x_test = np.expand_dims(x_train, -1), np.expand_dims(x_test, -1)         |
|             keras.Input(shape=(28, 28, 1)),                                           |                                                                                       |
|                                                                                       |                                                                                       |
|             layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),                 |     y_train = keras.utils.to_categorical(y_train, configs.num_classes)                |
|                                                                                       |     y_test = keras.utils.to_categorical(y_test, configs.num_classes)                  |
|             layers.MaxPooling2D(pool_size=(2, 2)),                                    |                                                                                       |
|                                                                                       |                                                                                       |
|             layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),                 |     model = keras.Sequential(                                                         |
|                                                                                       |                                                                                       |
|             layers.MaxPooling2D(pool_size=(2, 2)),                                    |         [                                                                             |
|                                                                                       |                                                                                       |
|             layers.Flatten(),                                                         |             keras.Input(shape=configs.image_shape),                                   |
|                                                                                       |                                                                                       |
|             layers.Dropout(0.5),                                                      |             layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),                 |
|                                                                                       |                                                                                       |
|             layers.Dense(configs.num_classes, activation="softmax"),                  |             layers.MaxPooling2D(pool_size=(2, 2)),                                    |
|                                                                                       |                                                                                       |
|         ]                                                                             |             layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),                 |
|                                                                                       |                                                                                       |
|     )                                                                                 |             layers.MaxPooling2D(pool_size=(2, 2)),                                    |
|                                                                                       |                                                                                       |
|                                                                                       |             layers.Flatten(),                                                         |
|     model.compile(                                                                    |                                                                                       |
|                                                                                       |             layers.Dropout(0.5),                                                      |
|         loss="categorical_crossentropy",                                              |                                                                                       |
|                                                                                       |             layers.Dense(configs.num_classes, activation="softmax"),                  |
|         optimizer="adam",                                                             |                                                                                       |
|                                                                                       |         ]                                                                             |
|         metrics=("accuracy",),                                                        |                                                                                       |
|                                                                                       |     )                                                                                 |
|     )                                                                                 |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |     model.compile(                                                                    |
|     model.summary()                                                                   |                                                                                       |
|                                                                                       |         loss="categorical_crossentropy",                                              |
|                                                                                       |                                                                                       |
|     training_history = model.fit(                                                     |         optimizer="adam",                                                             |
|                                                                                       |                                                                                       |
|         x_train, y_train,                                                             |         metrics=("accuracy",),                                                        |
|                                                                                       |                                                                                       |
|         epochs=15,                                                                    |     )                                                                                 |
|                                                                                       |                                                                                       |
|         batch_size=128,                                                               |                                                                                       |
|                                                                                       |     model.summary()                                                                   |
|         validation_split=0.1,                                                         |                                                                                       |
|                                                                                       |                                                                                       |
|     )                                                                                 |     training_history = model.fit(                                                     |
|                                                                                       |                                                                                       |
|                                                                                       |         x_train, y_train,                                                             |
|     test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)              |                                                                                       |
|                                                                                       |         epochs=configs.epochs,                                                        |
|                                                                                       |                                                                                       |
|     print(f"Test loss: {test_loss}")                                                  |         batch_size=configs.batch_size,                                                |
|                                                                                       |                                                                                       |
|     print(f"Test accuracy: {test_accuracy}")                                          |         validation_split=configs.val_dataset_fraction,                                |
|                                                                                       |                                                                                       |
|                                                                                       |         callbacks=(                                                                   |
|                                                                                       |                                                                                       |
| if __name__ == "__main__":                                                            |             TensorflowTrainingTracker(experiment),                                    |
|                                                                                       |                                                                                       |
|     train()                                                                           |         )                                                                             |
|                                                                                       |                                                                                       |
|                                                                                       |     )                                                                                 |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |     experiment.log_artifact("training_history.pkl", training_history)                 |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |     test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)              |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |     print(f"Test loss: {test_loss}")                                                  |
|                                                                                       |                                                                                       |
|                                                                                       |     print(f"Test accuracy: {test_accuracy}")                                          |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       |                                                                                       |
|                                                                                       | if __name__ == "__main__":                                                            |
|                                                                                       |                                                                                       |
|                                                                                       |     train()                                                                           |
+---------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------+

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