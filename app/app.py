import pygame
from gamemap import *

# Define colors for different terrain types
TERRAIN_COLORS = {
    "grass": (34, 139, 34),  # Green
    "water": (30, 144, 255),  # Blue
    "mountain": (139, 137, 137),  # Gray
}

# Define the size of the map and tiles
MAP_SIZE = 32
TILE_SIZE = 30


def dist_to_color(d):
    red = 10 * d + 34
    if red > 255:
        red = 255
    color = (red, 139, 34)
    return color


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
                    terrain_color = dist_to_color(
                        game_map.point_distance((i, j), (16, 16))
                    )
                # Draw the tile
                pygame.draw.rect(
                    game_display, terrain_color, (x, y, TILE_SIZE, TILE_SIZE)
                )
                pygame.draw.rect(
                    game_display, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 1
                )

        # Update the display
        pygame.display.update()

    # Quit the game
    pygame.quit()
