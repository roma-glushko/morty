from typing import Callable, List, Dict


class Signal:
    """
    Represents a way to send and subscribe to a signal
    """
    def __init__(self):
        self.receivers: List[Callable] = []

    def send(self, *arg, **kwargs):
        """
        Sends a signal with params
        """
        for receiver in self.receivers:
            receiver(*arg, **kwargs)

    def subscribe(self, subscriber: Callable):
        """
        Subscribes to a signal
        """
        self.receivers.append(subscriber)


signals: Dict[str, Signal] = {}


def signal(signal_name: str) -> Signal:
    """
    Retrieves a signal by name
    """
    if signal_name not in signals:
        signals[signal_name] = Signal()

    return signals[signal_name]


def subscriber(signal_name: str) -> Callable:
    """
    Registers a new subscriber function for the signal_name
    """
    def decorate_subscriber(subscriber_func: Callable) -> Callable:
        signal(signal_name).subscribe(subscriber_func)

        return subscriber_func

    return decorate_subscriber


__all__ = ("signal", "subscriber",)
