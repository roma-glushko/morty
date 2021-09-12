from unittest.mock import Mock

from morty.config import config, ConfigManager


def test__decorators__config_decorator_default_use():
    config_func = Mock()

    @config()
    def main_func(config: ConfigManager):
        config_func(config.args.__dict__)

    main_func()
    config_func.assert_called_once()


def test__decorators__config_decorator_with_path():
    pass


def test__decorators__config_decorator_with_path_and_name():
    pass


def test__decorators__config_decorator_with_custom_arg_parser():
    pass
