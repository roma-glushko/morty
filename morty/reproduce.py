import os
import random

import numpy as np

from morty.utils import is_tf_available

# Everything we need to make experiments more reproducible


def set_random_seed(seed: int = 42) -> None:
    """
    Fix globally all possible sources of randomness to keep experiment reproducible
    """
    os.environ["PYTHONHASHSEED"] = str(seed)

    random.seed(seed)
    np.random.seed(seed)

    if is_tf_available():
        os.environ["TF_DETERMINISTIC_OPS"] = "1"
        os.environ["TF_CUDNN_DETERMINISTIC"] = "1"

        import tensorflow

        tensorflow.random.set_seed(seed)
