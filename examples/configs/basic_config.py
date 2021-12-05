from dataclasses import dataclass
from typing import Tuple

from morty.config import BaseConfig


@dataclass
class Config(BaseConfig):
    test_run: bool = False
    num_classes: int = 10
    image_shape: Tuple[int, int, int] = (28, 28, 1)
    val_dataset_fraction: float = 0.1
    epochs: int = 3
    batch_size: int = 128
    optimizer: str = "adam"
    learning_rate: float = 1e-4


@dataclass
class TestConfig(Config):
    test_run = True
