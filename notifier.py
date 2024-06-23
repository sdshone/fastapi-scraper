from abc import ABC, abstractmethod

# Abstract class for notification strategy
class Notifier(ABC):
    """
    Abstract base class for a notification strategy.
    """
    @abstractmethod
    def notify(self, message: str):
        """
        Send a notification with the given message.
        """
        raise NotImplementedError

class ConsoleNotifier(Notifier):
    """
    Console-based notification implementation.
    """
    def notify(self, message: str):
        """
        Send a notification with the given message.
        """
        print(message)
