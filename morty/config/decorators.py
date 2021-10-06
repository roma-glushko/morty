import functools
from argparse import ArgumentParser
from typing import Any, Callable, Optional

from morty.config.args_parser import get_arg_parser
from morty.config.managers import ConfigManager

RunFunction = Callable[[Any], Any]


def config(
    path: str = "configs",
    name: str = "base_config",
    argument_parser: Optional[ArgumentParser] = None,
) -> Callable[[RunFunction], Any]:
    """
    Decorates main() function in order to load configs from py file
    @see https://github.com/facebookresearch/hydra/blob/master/hydra/main.py
    """

    def decorate_main_func(run_func: RunFunction) -> Callable[[], None]:
        @functools.wraps(run_func)
        def decorate_main_func(configs: Optional[ConfigManager] = None) -> Any:
            if configs is not None:
                # todo: document this case or remove it
                return run_func(configs)

            arg_parser = argument_parser

            if arg_parser is None:
                arg_parser = get_arg_parser()

            run_func_with_config(
                args_parser=arg_parser,
                run_func=run_func,
                config_path=path,
                config_name=name,
            )

        return decorate_main_func

    return decorate_main_func


def run_func_with_config(
    args_parser: ArgumentParser,
    run_func: RunFunction,
    config_path: str,
    config_name: str,
) -> None:
    """
    Run main() function with config manager instance loaded from specified place
    """
    args = args_parser.parse_args()

    if args.config_name is not None:
        config_name = args.config_name

    if args.config_path is not None:
        config_path = args.config_path

    configs = ConfigManager(config_path, config_name, console_args=args.__dict__)

    run_func(configs)
