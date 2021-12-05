from dataclasses import dataclass, asdict


@dataclass
class BaseConfig:
    """
    Marker class for morty configs that can be load from file
    """

    def dict(self) -> dict:
        return asdict(self)