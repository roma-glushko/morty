import importlib.util

_tf_available = importlib.util.find_spec("tensorflow") is not None


def is_tf_available() -> bool:
    return _tf_available
