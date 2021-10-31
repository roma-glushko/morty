import os
import random
import numpy as np
import tensorflow as tf

from morty import set_random_seed


def test__reproduce__set_seed():
    seed: int = 123

    set_random_seed(seed)

    assert os.environ["PYTHONHASHSEED"] == str(seed)
    assert os.environ["TF_DETERMINISTIC_OPS"] == "1"
    assert os.environ["TF_CUDNN_DETERMINISTIC"] == "1"

    assert random.uniform(1, 2) == 1.0523635988509443
    assert np.random.uniform(1, 2) == 1.6964691855978615
    # assert tf.random.uniform(1, 2) == seed
