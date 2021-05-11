from typing import Callable


class ComponentFactory:
    """
    ComponentFactory is a handy way to create a custom factory to
    create your ML components (losses, optimizers, feature extractors, etc) in a configurable way
    """

    component_registry = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        pass

    @classmethod
    def create(cls, name: str, **kwargs) -> Callable:
        pass