import importlib
import json
import os
import sys
from os.path import splitext
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, Optional

from attrdict import AttrDict


class ConfigManager:
    """
    ConfigManager is a handy way to gather your shared and private configs from different sources.
    """

    def __init__(
        self,
        config_path: str,
        config_name: str,
        console_args: Optional[Dict[str, Any]] = None,
    ):
        self._validate_config_path(config_path)

        config_args = self._load_config(config_path, config_name)

        if console_args is None:
            console_args = {}

        # todo: console args that were not specified can override configs with None values

        # merge configs from all sources
        self.args = AttrDict(
            {
                **config_args,
                **console_args,
                "config_file": os.path.join(config_path, config_name),
            }
        )

    @staticmethod
    def _load_config(config_path, config_name):
        sys.path.append(config_path)

        config_module = importlib.import_module(config_name)

        if not hasattr(config_module, "args"):
            msg = dedent(
                f"""\
            '{Path(config_path) / config_name}' config file should have 'args' dictionary declared
            """
            )

            raise RuntimeError(msg)

        return config_module.args

    @staticmethod
    def _validate_config_path(config_path: Optional[str]) -> None:
        if config_path is None:
            return

        split_file = splitext(config_path)

        if split_file[1] == ".py":
            # todo: process this case instead of warning
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

    def __getattr__(self, name):
        return getattr(self.args, name)

    def __iter__(self):
        for key, item in self.args.items():
            yield key, item

    def __repr__(self):
        return f"ConfigManager({json.dumps(self.args, indent=2, default=str)})"


class NotebookConfigManager:
    """
    NotebookConfigManager is designed to receive all configs from separate dictionary passed as a constructor argument.
    """

    def __init__(self, args: Dict[str, Any]):
        self.args = AttrDict(args)

    def __getattr__(self, name):
        return getattr(self.args, name)

    def __iter__(self):
        for key, item in self.args.items():
            yield key, item

    def __repr__(self):
        return f"NotebookConfigManager({json.dumps(self.args, indent=2)})"
