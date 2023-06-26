from abc import ABC, abstractmethod


# Define the interface using an abstract base class
class CommandPortInterface(ABC):
    @abstractmethod
    def get_commands(self):
        pass
