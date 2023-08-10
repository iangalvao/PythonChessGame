from abc import ABC, abstractmethod


class CommandHandlerInterface(ABC):
    @abstractmethod
    def walk(self, args):
        pass
