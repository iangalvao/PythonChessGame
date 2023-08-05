from app.entities.unit import *
from app.entities.gamemap import GameMap, Tile
from abc import ABC, abstractmethod
from app.utilities.coordinates import Coordinate


class UnitHandlerInterface:
    @abstractmethod
    def walk(self, unit, direction):
        pass


class UnitHandler:
    def __init__(self, gamemap, units, presenter) -> None:
        self.map = gamemap
        self.units = units
        self.presenter = presenter

    def walk(self, unit_id, direction):
        if direction.x not in (0, 1) or direction.y not in (0, 1):
            raise ValueError(
                f"unit_handler.wakr direction arg components should be 0 or 1: {direction}"
            )
        unit = self.getUnitByID(unit_id)
        x, y = (unit.pos.x, unit.pos.x)
        new_x, new_y = (x + direction.x, y + direction.y)

        self.move_unit(unit, Coordinate(new_x, new_y))

        # self.presenter.send_event("walk", unit, (new_x, new_y))
        self.presenter.walk(unit_id, (new_x, new_y))

    def move_unit(self, unit, pos):
        if self.map.out_of_bounds((pos.x, pos.y)):
            raise ValueError("Moving unit to position out of bounds!")
        if unit.pos == pos:
            raise ValueError("Moving unit to it's own position!")
        tile = unit.tile
        new_tile = self.map.tiles[pos.x][pos.y]

        new_tile.add_unit(unit)
        tile.remove_unit(unit.id)

    def getUnitByID(self, unit_id):
        return self.units[unit_id]
