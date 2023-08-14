from app.entities.match import Match
from typeguard import typechecked
from abc import ABC, abstractmethod
from app.entities.player import Player
from app.presenters.presenterInterface import PresenterInterface


class MatchHandlerInterface(ABC):
    @abstractmethod
    def next_turn(self):
        pass


class MatchHandler(MatchHandlerInterface):
    def __init__(self, match: Match, presenter: PresenterInterface) -> None:
        self.match = match
        self.presenter = presenter

    def next_turn(self):
        self.match.next_turn()
        self.presenter.next_turn(self.match.turn)
        self.start_turn(self.match.get_active_player())

    @typechecked
    def start_turn(self, player: Player):
        pass
