import importlib
import sys
from dataclasses import is_dataclass
from inspect import isclass
from pathlib import Path
from typing import Any, Generic, Optional, Type, TypeVar, Union

import click
import typer
from click import Context, Parameter, ParamType
from typer import Argument, Option, run
from typer.main import lenient_issubclass
from typer.models import ParameterInfo

from morty.config import BaseConfig

_original_get_click_type = typer.main.get_click_type


ConfigT = TypeVar("ConfigT", bound=BaseConfig)

ModuleTypes = Union[Type[ConfigT]]


class ConfigLoader(Generic[ConfigT], ParamType):
    name = "config"

    def convert(
        self, value: Any, param: Optional["Parameter"], ctx: Optional["Context"]
    ) -> Any:
        config = value

        if isclass(config) and issubclass(config, BaseConfig):
            return config()

        if is_dataclass(config):
            return config

        if isinstance(config, str) and "::" in config:
            # deal with path to config module
            module_path, config_classname = config.split("::")
            module_file: Path = Path(module_path + ".py")

            if not module_file.exists():
                ValueError()

            return self.load_from_module_file(module_file, config_classname)()

        raise ValueError()

    def load_from_module_file(
        self, module_file: Path, config_classname: str
    ) -> Type[ConfigT]:
        module_name: str = module_file.stem
        package_name: str = str(module_file.parent.absolute())

        sys.path.append(package_name)

        config_module = importlib.import_module(module_name)

        if not hasattr(config_module, config_classname):
            raise ValueError()

        return getattr(config_module, config_classname)

    def __repr__(self) -> str:
        return "ConfigConvertor"


def get_click_type(
    *, annotation: Any, parameter_info: ParameterInfo
) -> click.ParamType:
    if lenient_issubclass(annotation, BaseConfig):
        return ConfigLoader()

    return _original_get_click_type(
        annotation=annotation, parameter_info=parameter_info
    )


typer.main.get_click_type = get_click_type

__all__ = ("Option", "Argument", "run")
