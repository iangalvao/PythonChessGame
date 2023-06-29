from entities.unit import *
from entities.gamemap import GameMap, Tile


class UnitHandler:
    def __init__(self, gamemap) -> None:
        self.map = gamemap

    def move_unit(self, args):
        unit_id, direction = args
        unit = self.get_by_id(unit_id)
        x, y = unit.pos
        tile = self.map.tiles[x][y]
        tile.remove_unit(unit)
        new_x, new_y = (x + direction[0], y + direction[1])
        new_tile = self.map.tiles[new_x][new_y]
        new_tile.add_unit(unit)
        unit.pos = (new_x, new_y)
