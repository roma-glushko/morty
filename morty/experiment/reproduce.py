import os
import numpy as np
import tensorflow as tf

"""
Everything we need to make experiments more reproducible
"""

def set_random_seed(seed=42):
    """
    Globally fix all possible sources of randomness to keep experiment reproducible 
    """
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_DETERMINISTIC_OPS'] = '1'