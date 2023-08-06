from abc import ABC, abstractmethod


class PresenterInterface(ABC):
    @abstractmethod
    def walk(self, unit_id, pos):
        pass

    def show_error_message(self, s: str):
        pass
