import json
import os
import sys
import importlib
from textwrap import dedent

from attrdict import AttrDict


class ConfigManager:
    """
    ConfigManager is a handy way to gather your shared and private configs from different sources.
    """

    def __init__(self, config_path: str, config_name: str):
        args = self.load_config(config_path, config_name)

        args['config_file'] = os.path.join(config_path, config_name)

        self.args = AttrDict(args)

    @staticmethod
    def load_config(config_path, config_name):
        sys.path.append(config_path)

        config_module = importlib.import_module(config_name)

        if not hasattr(config_module, 'args'):
            msg = dedent(
                """\
            config_name should have args dictionary declared
            """
            )

            raise RuntimeError(msg)

        return config_module.args

    def __getattr__(self, name):
        return getattr(self.args, name)

    def __repr__(self):
        return 'ConfigManager({})'.format(json.dumps(self.args, indent=2))


class NotebookConfigManager:
    """
    NotebookConfigManager is designed to receive all configs from separate dictionary passed as a constructor argument.
    """

    def __init__(self, args):
        self.args = AttrDict(args)

    def __getattr__(self, name):
        return getattr(self.args, name)

    def __repr__(self):
        return 'NotebookConfigManager({})'.format(json.dumps(self.args, indent=2))