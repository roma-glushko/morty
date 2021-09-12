from typing import Any, Optional

from morty.experiment import Experiment


class ExperimentManager:
    """
    Performs high level operations like experiment creation or loading
    """

    def __init__(self, root_dir: str = "./experiments", configs: Optional[Any] = None):
        """ """
        self.root_directory = root_dir
        self.configs = configs

    def create(self) -> Experiment:
        """
        Create a new experiment
        """
        experiment: Experiment = Experiment(self.root_directory)

        experiment.start()

        if self.configs:
            experiment.log_configs(self.configs)

        return experiment
