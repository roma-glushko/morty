from dataclasses import is_dataclass, asdict
from datetime import datetime
from json import JSONEncoder
from typing import Set

from morty.config import BaseConfig

json_encoders = {
    datetime: lambda o: str(o.isoformat()),
    BaseConfig: lambda o: o.dict(),
    Set: lambda o: list(o),
    type: lambda o: f"{o.__module__}.{o.__class__}"
}


class ExperimentEncoder(JSONEncoder):
    def default(self, obj):
        for classname, encoder in json_encoders.items():
            if isinstance(obj, classname):
                return encoder(obj)

        if is_dataclass(obj):
            return asdict(obj)

        return JSONEncoder.default(self, obj)
