from math import ceil
from typing import List
from typeguard import typechecked
from app.entities.tile import Tile
from app.utilities.coordinates import Coordinate


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

    @typechecked
    def get_tile(self, pos: Coordinate) -> Tile:
        return self.tiles[pos.x][pos.y]

    @typechecked
    def point_distance(self, posA: Coordinate, posB: Coordinate) -> float:
        if self.out_of_bounds(posA) or self.out_of_bounds(posB):
            raise ValueError("Invalid coordinates")
        x_dist = abs(posA.x - posB.x)
        y_dist = abs(posA.y - posB.y)
        return max(x_dist + y_dist / 2, x_dist / 2 + y_dist)

    @typechecked
    def get_neighbours(self, center_pos: Coordinate, radius: float) -> List[Tile]:
        if self.out_of_bounds(center_pos):
            raise ValueError("Invalid coordinates")

        neighbors = []
        search_radius = ceil(radius)

        # Iterate over the tiles within the search radius
        for i in range(-search_radius, search_radius + 1):
            for j in range(-search_radius, search_radius + 1):
                # Skip the center tile
                if i == 0 and j == 0:
                    continue

                # Calculate the coordinates of the neighbor candidate tile.
                neighbor = Coordinate(center_pos.x + i, center_pos.y + j)
                # Check if the neighboring tile is within the map boundaries
                if not self.out_of_bounds(neighbor):
                    # Check if the neighboring tile is within given radius
                    if self.point_distance(center_pos, neighbor) <= radius:
                        neighbors.append(self.get_tile(neighbor))

        return neighbors

    @typechecked
    def out_of_bounds(self, pos: Coordinate) -> bool:
        if pos.x < 0 or pos.x >= self.size or pos.y < 0 or pos.y >= self.size:
            return True
        return False


class TerrainGenerator:
    def __init__(self, gen_function) -> None:
        self.generate_ = gen_function

    def generate(self, map: GameMap) -> None:
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
