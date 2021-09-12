from morty.config import NotebookConfigManager


def test__config_manager__init_notebook_config_manager():
    config = NotebookConfigManager({
        "config_name": "Test Config",
        "batch_size": 64,
    })

    assert config.config_name == "Test Config"
    assert config.batch_size == 64