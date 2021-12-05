import warnings
from contextlib import suppress
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Iterable, Set

from morty import Experiment
from morty.dashboard.summarizers import summarize_trainings
from morty.exceptions import IndexWarning

@dataclass
class IndexEntry:
    last_updated_at: datetime
    data: Dict[str, Any]

@dataclass
class ExperimentIndex:
    last_updated_at: datetime
    columns: Set[str]
    experiments: Dict[str, IndexEntry]


def reindex_experiments(experiments: Iterable[Experiment]) -> ExperimentIndex:
    updated_at: datetime = datetime.utcnow()
    columns: Set[str] = set()
    experiment_index: Dict[str, IndexEntry] = {}

    for experiment in experiments:
        try:
            meta = experiment.meta
            configs = experiment.configs
            train_summary = summarize_trainings(experiment.train_runs)

            git = {}

            with suppress(OSError):
                git = asdict(experiment.git)

            experiment_data = {
                **asdict(meta),
                **git,
                **configs,
                **train_summary,
            }

            experiment_index[meta.experiment_id] = IndexEntry(
                last_updated_at=max(meta.train_runs),
                data=experiment_data,
            )

            columns.update(set(experiment_data.keys()))
        except Exception as e:
            print(e.__class__.__name__)
            warnings.warn(
                f"Cannot index '{experiment.experiment_id}' experiment: {str(e)} \n "
                "Skipping the experiment information",
                IndexWarning,
            )

    return ExperimentIndex(
        last_updated_at=updated_at,
        columns=columns,
        experiments=experiment_index,
    )
