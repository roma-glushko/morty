from typing import Dict, Union

from pydantic import BaseModel


class MetricSummary(BaseModel):
    """
    Summarizes a single metric
    Example:
        {
            "metric": "loss",
            summaries: {
                "max": 0.865,
                "min": 0.124,
            }
        }
    """

    metric: str
    summaries: Dict[str, Union[int, float]]


class TrainingSummary(BaseModel):
    """
    Summaries the whole training process
    """

    epoch: int
    metrics: Dict[str, MetricSummary]
