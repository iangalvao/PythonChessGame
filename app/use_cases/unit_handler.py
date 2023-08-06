from typeguard import typechecked
from app.entities.unit import *
from app.entities.gamemap import GameMap, Tile
from abc import ABC, abstractmethod
from app.utilities.coordinates import Coordinate
from app.presenters.presenterInterface import PresenterInterface


class UnitHandlerInterface:
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

    # invalid coordinates (not in (-1,0,1))
    # invalid unit id (non existent)
    # valid input generate the right self calls (move_unit (id, coord+dir))
    # valid input generate the right walk calls (walk (id, coord+dir))
    # valid input but invalid unit pos should raise error (check olnly in move_unit )
    @typechecked
    def walk(self, unit_id: int, direction: Coordinate) -> None:
        if direction.x not in (-1, 0, 1) or direction.y not in (-1, 0, 1):
            raise ValueError(
                f"unit_handler.wakr direction arg components should be 0 or 1: {direction}"
            )
        try:
            unit = self.getUnitByID(unit_id)
            new_pos = unit.pos + direction

            self.move_unit(unit, new_pos)
            self.presenter.walk(unit_id, (new_pos.x, new_pos.y))

        except ValueError as e:
            # Handle the error, maybe log it for debugging purposes
            # and inform the user through the presenter
            self.presenter.show_error_message(str(e))

        # self.presenter.send_event("walk", unit, (new_x, new_y))

    @typechecked
    def move_unit(self, unit: Unit, pos: Coordinate) -> None:
        if self.map.out_of_bounds((pos.x, pos.y)):
            raise ValueError("Moving unit to position out of bounds!")
        if unit.pos == pos:
            raise ValueError("Moving unit to it's own position!")
        tile = unit.tile
        new_tile = self.map.tiles[pos.x][pos.y]

        new_tile.add_unit(unit)
        tile.remove_unit(unit.id)

    @typechecked
    def getUnitByID(self, unit_id: int) -> Unit:
        return self.units[unit_id]
