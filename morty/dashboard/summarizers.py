from collections import Iterable, defaultdict
from typing import Dict, List

from pydantic.main import BaseModel


class ColumnStatistics(BaseModel):
    min: float = 0.0
    max: float = 0.0
    mean: float = 0.0
    # median: float = 0.0
    # std_deviation: float = 0.0


def summarize_trainings(train_readers: Iterable[Iterable[dict]]):
    """ """
    train_epochs: Dict[str, List[float]] = defaultdict(list)

    # build a dict with values from all train epochs across all train files

    for train_reader in train_readers:
        for epoch_row in train_reader:
            for column, value in epoch_row.items():
                train_epochs[column].append(float(value))

    statistics: Dict[str, ColumnStatistics] = {}

    for column, values in train_epochs.items():
        statistics[column] = ColumnStatistics(
            min=min(values), max=max(values), mean=sum(values) / len(values)
        )

    return statistics
