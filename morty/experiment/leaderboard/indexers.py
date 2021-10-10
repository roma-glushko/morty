import warnings
from datetime import datetime
from typing import Any, Dict, Set

from pydantic import BaseModel

from morty.experiment import ExperimentManager
from morty.experiment.exceptions import IndexWarning


class IndexEntry(BaseModel):
    last_updated_at: datetime
    data: Dict[str, Any]


class ExperimentIndex(BaseModel):
    columns: Set[str]
    experiments: Dict[str, IndexEntry]


class ExperimentIndexer:
    def reindex(self, experiment_manager: ExperimentManager):
        columns = set()
        experiments = {}

        for experiment in experiment_manager:
            try:
                meta = experiment.meta
                git = experiment.git
                configs = experiment.configs

                experiment_data = {
                    "created_at": meta.created_at,
                    "experiment_id": meta.experiment_id,
                    "branch": git.branch,
                    "commit": git.commit_hash,
                } | configs

                experiments[meta.experiment_id] = IndexEntry(
                    last_updated_at=meta.created_at,
                    data=experiment_data,
                )

                columns.update(set(experiment_data.keys()))
            except Exception as e:
                warnings.warn(
                    f"Cannot index '{experiment.experiment_id}' experiment: {str(e)} \n "
                    "Skipping the experiment",
                    IndexWarning,
                )

        index = ExperimentIndex(
            columns=columns,
            experiments=experiments,
        )

        experiment_manager.io.log_json()
