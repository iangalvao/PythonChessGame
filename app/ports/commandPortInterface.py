from abc import ABC, abstractmethod


# Define the interface using an abstract base class
class CommandPortInterface(ABC):
    @abstractmethod
    def get_line(self):
        pass

    def listen(self):
        pass
