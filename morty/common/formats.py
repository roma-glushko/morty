from collections import MutableMapping
from typing import Any, List, Tuple, Union


def flatten_dict(
    dictionary: MutableMapping,
    parent_key: Union[bool, str] = False,
    separator: str = ".",
) -> dict:
    """
    Turns a nested dictionary into a flattened dictionary
    """

    items: List[Tuple[str, Any]] = []

    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key

        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten_dict({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))

    return dict(items)
