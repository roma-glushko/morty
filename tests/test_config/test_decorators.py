import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from morty.config import config, ConfigManager
from tests.test_config.conftest import create_config_file


@patch("argparse._sys.argv")
def test__decorators__config_decorator_default_use(argv):
    config_func = Mock()
    argv.return_value = ["/Users/usr/examples/train.py"]

    root_dir = Path(tempfile.mkdtemp()) / "configs"
    create_config_file(root_dir, "base_config.py")

    @config(path=str(root_dir), name="base_config")
    def main_func(config: ConfigManager):
        config_func(config.args)

    main_func()
    config_func.assert_called_once()


@patch("argparse._sys.argv")
def test__decorators__config_decorator_with_path(argv):
    config_func = Mock()
    argv.return_value = ["/Users/usr/examples/train.py"]

    root_dir = Path(tempfile.mkdtemp()) / "configs"
    create_config_file(root_dir, "base_config.py")

    @config(path=str(root_dir))
    def main_func(config: ConfigManager):
        config_func(config.args)

    main_func()
    config_func.assert_called_once()


@patch("argparse._sys.argv")
def test__decorators__config_decorator_with_path_and_name(argv):
    config_func = Mock()
    argv.return_value = ["/Users/usr/examples/train.py"]

    root_dir = Path(tempfile.mkdtemp()) / "configs"
    create_config_file(root_dir, "config.py")

    @config(path=str(root_dir), name="config")
    def main_func(config: ConfigManager):
        config_func(config.args)

    main_func()
    config_func.assert_called_once()


@patch("argparse._sys.argv")
def test__decorators__config_decorator_with_console_args(argv):
    config_func = Mock()

    root_dir = Path(tempfile.mkdtemp()) / "settings"
    create_config_file(root_dir, "base_config.py")

    argv.return_value = [
        "/Users/usr/examples/train.py",
        "--config_path",
        root_dir,
        "--config_name",
        "base_config",
    ]

    @config()
    def main_func(config: ConfigManager):
        config_func(config.args)

    main_func()
    config_func.assert_called_once()


def test__decorators__config_decorator_with_custom_arg_parser():
    pass
