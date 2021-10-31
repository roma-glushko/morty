import json
import pickle
from json import JSONEncoder
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Iterable, List, Type, Union

from pydantic import BaseModel

from morty.common.serialize import ExperimentEncoder


class Directory:
    """
    Abstracts away all specific of working with filesystem
    """

    def __init__(
        self,
        dir_path: PathLike,
        encoder_class: Type[JSONEncoder] = ExperimentEncoder,
    ):
        self.dir_path = Path(dir_path)
        self.encoder_class = encoder_class

        self.dir_path.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, file_name: str) -> Path:
        """
        Retrieve a path to the current experiment directory
        """
        return self.dir_path / file_name

    def log_binary(self, file_name: str, binary: Any):
        """
        Log an object as a binary file
        """
        binary_path: Path = self.get_file_path(file_name)
        pickle.dump(binary, open(binary_path, "wb"))

    def get_binary(self, file_name) -> Any:
        binary_path: Path = self.get_file_path(file_name)

        try:
            return pickle.load(open(binary_path, "rb"))
        except Exception as e:
            raise IOError(f"Failed to open {binary_path}: {str(e)}")

    def log_json(
        self, data: Union[Dict, BaseModel], filename: str, file_ext: str = "json"
    ):
        """
        Save data as JSON file
        """
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        json.dump(
            data,
            open(output_path, "w"),
            indent=4,
            sort_keys=True,
            cls=self.encoder_class,
        )

    def get_json(self, filename: str, file_ext: str = "json") -> Dict:
        file_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        try:
            return json.load(open(file_path, "r"))
        except Exception as e:
            raise IOError(f"Failed to open {file_path}: {str(e)}")

    def log_text(self, lines: Iterable[str], filename: str, file_ext: str = "txt"):
        """
        Log strings as a plain text
        """
        output_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        with open(output_path, "a") as output_file:
            output_file.writelines(lines)

    def get_text(self, filename: str, file_ext: str = "txt") -> List[str]:
        file_path: Path = self.get_file_path(f"{filename}.{file_ext}")

        try:
            return open(file_path, "r").readlines()
        except Exception as e:
            raise IOError(f"Failed to open {file_path}: {str(e)}")
