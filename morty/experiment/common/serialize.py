from datetime import datetime
from json import JSONEncoder

from pydantic import BaseModel

json_encoders = {
    datetime: lambda o: str(o.isoformat()),
    BaseModel: lambda o: o.dict(),
}


class ExperimentEncoder(JSONEncoder):
    def default(self, obj):
        for classname, encoder in json_encoders.items():
            if isinstance(obj, classname):
                return encoder(obj)

        return JSONEncoder.default(self, obj)
