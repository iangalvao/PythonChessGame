from abc import ABC, abstractmethod


class CommandHandlerInterface(ABC):
    @abstractmethod
    def parse_line(self, input_line):
        pass
