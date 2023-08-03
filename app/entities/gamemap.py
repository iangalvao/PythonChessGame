from math import ceil, floor

from app.utilities.coordinates import Coordinate


class Tile:
    def __init__(self, pos):
        self.terrain = None
        self.terrain_overlay = None
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

    def set_pos(self, pos):
        self.pos = pos

    def set_units(self, units):
        self.units = units

    def set_settlement(self, settlement):
        self.settlement = settlement

    def get_terrain(self):
        return self.terrain

    def set_terrain(self, terrain):
        self.terrain = terrain

    def add_unit(self, unit):
        self.units[unit.id] = unit
        unit.tile = self
        unit.pos = self.pos

    def remove_unit(self, unit_id):
        self.units.pop(unit_id)


class GameMap:
    def __init__(self, size, map_generator=None) -> None:
        self._size = size
        self._tiles = [
            [Tile(Coordinate(i, j)) for j in range(size)] for i in range(size)
        ]
        if map_generator:
            map_generator.generate(self)

    @property
    def size(self):
        return self._size

    @property
    def tiles(self):
        return self._tiles

    def point_distance(self, posA, posB):
        if self.out_of_bounds(posA) or self.out_of_bounds(posB):
            raise ValueError("Invalid coordinates")
        x_dist = abs(posA[0] - posB[0])
        y_dist = abs(posA[1] - posB[1])
        return max(x_dist + y_dist / 2, x_dist / 2 + y_dist)

    def get_neighbours(self, pos, radius):
        # Check if the position is out of bounds
        if self.out_of_bounds(pos):
            raise ValueError("Invalid coordinates")

        neighbors = []
        center_x, center_y = pos
        search_radius = ceil(radius)

        # Iterate over the tiles within the search radius
        for i in range(-search_radius, search_radius + 1):
            for j in range(-search_radius, search_radius + 1):
                # Skip the center tile
                if i == 0 and j == 0:
                    continue

                # Calculate the coordinates of the neighboring tile
                neighbor_x = center_x + i
                neighbor_y = center_y + j

                neighbor = (neighbor_x, neighbor_y)
                # Check if the neighboring tile is within the map boundaries
                if not self.out_of_bounds(neighbor):
                    # Check if the neighboring tile is within given radius
                    if self.point_distance(neighbor, pos) <= radius:
                        neighbors.append(self._tiles[neighbor_x][neighbor_y])

        return neighbors

    def out_of_bounds(self, pos):
        i, j = pos[0], pos[1]
        if i < 0 or i >= self.size or j < 0 or j >= self.size:
            return True
        return False


class TerrainGenerator:
    def __init__(self, gen_function) -> None:
        self.generate_ = gen_function

    def generate(self, map):
        self.generate_(map)


def generate_square_land(map):  # Assign terrain types randomly
    for i in range(map.size):
        for j in range(map.size):
            terrain_type = "grass"  # Default terrain type
            # Assign different terrain types based on some conditions
            # You can define your own logic here for assigning terrain types
            if i < 5 or i > 25 or j < 5 or j > 25:
                terrain_type = "water"
            elif i == 15 and j == 15:
                terrain_type = "mountain"
            map.tiles[i][j].set_terrain(terrain_type)
