from app.entities.unit import Unit
from app.utilities.coordinates import Coordinate
from typeguard import typechecked


class Tile:
    def __init__(self, pos: Coordinate):
        self.set_terrain(None)
        self.set_terrain_overlay(None)
        self.rivers = []
        self.resource = None
        self.improvements = []

        self.pos = pos

        self.units = {}
        self.settlement = None

    # Getters
    def get_terrain(self):
        return self.terrain

    def get_terrain_overlay(self):
        return self.terrain_overlay

    def get_rivers(self):
        return self.rivers

    def get_resource(self):
        return self.resource

    def get_improvements(self):
        return self.improvements

    def get_pos(self):
        return self.pos

    def get_units(self):
        return self.units

    def get_settlement(self):
        return self.settlement

    # Setters
    def set_terrain(self, terrain):
        self.terrain = terrain

    def set_terrain_overlay(self, overlay):
        self.terrain_overlay = overlay

    def add_river(self, river):
        self.rivers.append(river)

    def set_resource(self, resource):
        self.resource = resource

    def add_improvement(self, improvement):
        self.improvements.append(improvement)

    def set_pos(self, pos: Coordinate):
        self.pos = pos

    def set_units(self, units):
        self.units = units

    def set_settlement(self, settlement):
        self.settlement = settlement

    def get_terrain(self):
        return self.terrain

    def set_terrain(self, terrain):
        self.terrain = terrain

    @typechecked
    def add_unit(self, unit: Unit):
        assert isinstance(
            unit.id, str
        ), f'"unit.id" ({type(unit.id)}) is not an instance of str'
        self.units[unit.id] = unit

    @typechecked
    def remove_unit(self, unit_id: str):
        self.units.pop(unit_id)
