from typing import Dict, Any, Iterator, Tuple, Iterable

from tabulate import tabulate


class ComponentFactory(Iterable[Tuple[str, Any]]):
    """
    ComponentFactory is a handy way to create a custom factory to
    create your ML components (losses, optimizers, feature extractors, etc) in a configurable way.

    Inspired by: https://github.com/facebookresearch/fvcore/blob/master/fvcore/common/registry.py

    To create a registry (e.g. a scheduler registry):
    .. code-block:: python
        scheduler_factory = ComponentFactory('scheduler')

    To register an object:
    .. code-block:: python
        @scheduler_factory.register()
        class CosineScheduler():
            ...
    Or:
    .. code-block:: python
        scheduler_factory.register(CosineScheduler)
    """
    component_map: Dict[str, Any] = {}

    def __init__(self, factory_name: str) -> None:
        """
        Args:
            factory_name (str): Name of the current factory (used in exceptions)
        """
        self.factory_name: str = factory_name

    def register(self, component_name: str = None, component: Any = None) -> Any:
        """
        Entry point for registering component classes and functions. Can be called directly or as a decorator

        Args:
            component_name (str): User-friendly name of the component
            component (Any): component represented as a class or a function
        """
        if component is not None:
            name = component.__name__ if component_name is None else component_name
            self.register_component(name, component)

            return component

        # used as a decorator
        def decorate_component(component: Any) -> Any:
            name = component.__name__ if component_name is None else component_name
            self.register_component(name, component)

            return component

        return decorate_component

    def register_component(self, component_name: str, component: Any) -> None:
        assert (component_name not in self.component_map), \
            "An object named '{}' was already registered in '{}' factory!".format(component_name, self.factory_name)

        self.component_map[component_name] = component

    def get(self, component_name: str) -> Any:
        """Retrieve component by name"""
        component = self.component_map.get(component_name)

        if component is None:
            raise KeyError(
                "No object named '{}' found in '{}' registry!".format(component, self.factory_name)
            )

        return component

    def __contains__(self, component_name: str) -> bool:
        return component_name in self.component_map

    def __repr__(self) -> str:
        """Render component map as a table"""
        table = tabulate(
            self.component_map.items(),
            headers=["Names", "Components"],
            tablefmt="fancy_grid"
        )

        return "Factory of {}:\n".format(self.factory_name) + table

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Iterate through component map"""
        return iter(self.component_map.items())
