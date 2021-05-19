import functools
import os
from argparse import ArgumentParser
from os.path import splitext
from textwrap import dedent
from typing import Callable, Optional, Any

from .config_manager import ConfigManager
from .runner_arguments import get_arg_parser

RunFunction = Callable[[Any], Any]


def main(
        config_path: Optional[str] = None,
        config_name: Optional[str] = None,
        argument_parser: Optional[ArgumentParser] = None,
) -> Callable[[RunFunction], Any]:
    """
    @see https://github.com/facebookresearch/hydra/blob/master/hydra/main.py
    """

    def decorate_main_func(run_func: RunFunction) -> Callable[[], None]:
        @functools.wraps(run_func)
        def decorated_main(config: Optional[ConfigManager] = None) -> Any:
            if config is not None:
                # todo: document this case or remove it
                return run_func(config)

            arg_parser = argument_parser

            if arg_parser is None:
                arg_parser = get_arg_parser()

            run_func_with_config(
                args_parser=arg_parser,
                run_func=run_func,
                config_path=config_path,
                config_name=config_name,
            )

        return decorated_main

    return decorate_main_func


def validate_config_path(config_path: Optional[str]) -> None:
    if config_path is None:
        return

    split_file = splitext(config_path)

    if split_file[1] == ".py":
        msg = dedent(
            """\
        Using config_path to specify the config name is not supported, specify the config name via config_name.
        """
        )

        raise ValueError(msg)

    abs_config_path = os.path.abspath(config_path)

    if not os.path.isdir(abs_config_path):
        msg = dedent(
            """\
        config_path should be an accessible directory, make sure provided path is correct.
        """
        )

        raise ValueError(msg)


def run_func_with_config(
        args_parser: ArgumentParser,
        run_func: RunFunction,
        config_path: Optional[str],
        config_name: Optional[str],
) -> None:
    args = args_parser.parse_args()

    if args.config_name is not None:
        config_name = args.config_name

    if args.config_path is not None:
        config_path = args.config_path

    validate_config_path(config_path)

    config = ConfigManager(config_path, config_name)

    run_func(config)

