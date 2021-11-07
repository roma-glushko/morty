from datetime import datetime
from json import JSONEncoder
from typing import Set

from pydantic import BaseModel

from morty.config import ConfigManager

json_encoders = {
    datetime: lambda o: str(o.isoformat()),
    BaseModel: lambda o: o.dict(),
    ConfigManager: lambda o: dict(o.args),
    Set: lambda o: list(o),
}


class ExperimentEncoder(JSONEncoder):
    def default(self, obj):
        for classname, encoder in json_encoders.items():
            if isinstance(obj, classname):
                return encoder(obj)

        return JSONEncoder.default(self, obj)
