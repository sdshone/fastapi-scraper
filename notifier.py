class Notifier:
    def notify(self, message: str):
        raise NotImplementedError

class ConsoleNotifier(Notifier):
    def notify(self, message: str):
        print(message)
