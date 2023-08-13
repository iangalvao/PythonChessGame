from app.controllers.commandHandler import CommandHandler
from app.entities.gamemap import GameMap
from app.entities.unit import Unit
from app.utilities.coordinates import Coordinate
from app.ports.commandPort import CommandPort
from app.router.router import Router
from app.presenters.terminalPresenter import TerminalPresenter
from app.use_cases.unit_handler import UnitHandler


class Game:
    def __init__(self) -> None:
        gamemap = GameMap(5)
        unit = Unit(1, 0, "test_unit")

        terminal_presenter = TerminalPresenter()
        unit_handler = UnitHandler(gamemap, {1: unit}, terminal_presenter)

        unit_handler.add_unit_to_tile(unit, gamemap.get_tile(Coordinate(2, 2)))

        controller = CommandHandler(unit_handler)
        router = Router(controller)
        port = CommandPort(router)

        port.listen()
