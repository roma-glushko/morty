import os
import random

import numpy as np
import tensorflow as tf

# Everything we need to make experiments more reproducible


def set_random_seed(seed: int = 42) -> None:
    """
    Fix globally all possible sources of randomness to keep experiment reproducible
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    os.environ["TF_CUDNN_DETERMINISTIC"] = "1"

    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
