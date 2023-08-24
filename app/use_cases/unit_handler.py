from typeguard import typechecked
from app.entities.unit import *
from app.entities.gamemap import GameMap, Tile
from abc import ABC, abstractmethod
from app.utilities.coordinates import Coordinate
from app.presenters.presenterInterface import PresenterInterface


class UnitHandlerInterface(ABC):
    @abstractmethod
    def walk(self, unit, direction):
        pass


class UnitHandler:
    @typechecked
    def __init__(
        self, gamemap: GameMap, units: dict, presenter: PresenterInterface
    ) -> None:
        self.map = gamemap
        self.units = units
        self.presenter = presenter

    @typechecked
    def walk(self, unit_id: int, direction: Coordinate) -> None:
        if direction.x not in (-1, 0, 1) or direction.y not in (-1, 0, 1):
            raise ValueError(
                f"unit_handler.walk direction arg components should be -1, 0 or 1: {direction}"
            )

        # try:
        #    unit = self.getUnitByID(unit_id)
        #    new_pos = unit.pos + direction
        #    action = check_if_movable(tile, unit)
        #    if action == "move":
        #       self.move_unit(unit, new_pos)
        #    if action == "combat":
        #       self.attack(unit, new_pos)
        #    self.presenter.send_event(action + ...)
        # except ValueError as e:
        #   self.presenter.send_error_message(str(e))
        # except KeyError as e:
        #   self.presenter.send_error_message(str(e))

        try:
            unit = self.getUnitByID(unit_id)
            new_pos = unit.pos + direction

            self.move_unit(unit, new_pos)
            self.presenter.walk(unit_id, (new_pos.x, new_pos.y))

        except ValueError as e:
            self.presenter.show_error_message(str(e))

    @typechecked
    def move_unit(self, unit: Unit, pos: Coordinate) -> None:
        if self.map.out_of_bounds(pos):
            raise ValueError("Moving unit to position out of bounds!")
        if unit.pos == pos:
            raise ValueError("Moving unit to it's own position!")
        tile = unit.tile
        new_tile = self.map.get_tile(pos)
        self.add_unit_to_tile(unit, new_tile)
        tile.remove_unit(unit.id)

    @typechecked
    def getUnitByID(self, unit_id: int) -> Unit:
        if unit_id not in self.units.keys():
            raise ValueError("Could not locate requested unit.")
        return self.units[unit_id]

    @typechecked
    def add_unit_to_tile(self, unit: Unit, tile: Tile):
        tile.add_unit(unit)
        unit.tile = tile
        unit.pos = tile.pos

    @typechecked
    def next_turn(self, unit: Unit):
        pass
