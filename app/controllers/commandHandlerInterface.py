from abc import ABC, abstractmethod


class CommandHandlerInterface(ABC):
    @abstractmethod
    def execute(self, input_line):
        pass
