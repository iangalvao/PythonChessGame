import pygame
import math
from math import ceil, floor
# Define colors for different terrain types
TERRAIN_COLORS = {
    "grass": (34, 139, 34),  # Green
    "water": (30, 144, 255),  # Blue
    "mountain": (139, 137, 137),  # Gray
}

# Define the size of the map and tiles
MAP_SIZE = 32
TILE_SIZE = 30


class Tile():
    def __init__(self) -> None:
        self.terrain = None
    def get_terrain(self):
        return self.terrain
    def set_terrain(self, terrain):
        self.terrain = terrain


class GameMap():
    def __init__(self, size, map_generator = None) -> None:
        self._size = size
        self._tiles = [[Tile() for _ in range (size)] for _ in range(size)]
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
        x_dist = abs (posA[0] - posB[0])
        y_dist = abs (posA[1] - posB[1])
        return max(x_dist + y_dist/2, x_dist/2 + y_dist)

    def get_neighbours(self, pos, radius):
        
        # Check if the position is out of bounds
        if self.out_of_bounds(pos):
            raise ValueError("Invalid coordinates")
        
        neighbors = []
        center_x, center_y = pos
        search_radius = ceil(radius)

        # Iterate over the tiles within the search radius
        for i in range(-search_radius, search_radius+1):
            for j in range(-search_radius, search_radius+1):
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
        i,j = pos[0], pos[1]
        if i < 0 or i >= MAP_SIZE or j < 0 or j >= MAP_SIZE:
            return True
        return False


def distance(posA,posB):
    if unbound(posA) or unbound(posB):
        raise ValueError("Invalid coordinates")
    x_dist = abs (posA[0] - posB[0])
    y_dist = abs (posA[1] - posB[1])
    return max(x_dist + y_dist/2, x_dist/2 + y_dist)

def unbound(pos):
    i,j = pos[0], pos[1]
    if i < 0 or i >= MAP_SIZE or j < 0 or j >= MAP_SIZE:
        return True
    return False

def dist_to_color(d):
    red = 10*d+34
    if red > 255:
        red = 255
    color = (red, 139,34)
    return color

class TerrainGenerator():
    def __init__(self, gen_function) -> None:
        self.generate_ = gen_function
    def generate(self,map):
        self.generate_(map)


def generate_square_land(map):    # Assign terrain types randomly
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


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up the display
    display_width = MAP_SIZE * TILE_SIZE
    display_height = MAP_SIZE * TILE_SIZE
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Map with Terrain")

    # Create the map array with terrain types
    game_map = GameMap(MAP_SIZE, TerrainGenerator(generate_square_land))

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the map
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                # Calculate the position of the current tile
                x = i * TILE_SIZE
                y = j * TILE_SIZE
                # Get the color for the current terrain type
                terrain = game_map.tiles[i][j].terrain
                terrain_color = TERRAIN_COLORS[terrain]
                if terrain == "grass":
                    terrain_color = dist_to_color(distance((i,j),(16,16)))
                # Draw the tile
                pygame.draw.rect(game_display, terrain_color, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(game_display, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 1)

        # Update the display
        pygame.display.update()

    # Quit the game
    pygame.quit()
