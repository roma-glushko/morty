import tempfile

from morty import ExperimentManager


def test__experiment_manager__create_new_experiment():
    temp_root_dir = tempfile.mkdtemp()
    experiment = ExperimentManager(root_dir=temp_root_dir).create()

    assert experiment.get_directory().is_dir()


def test__experiment_manager__create_new_experiment_with_config():
    pass
