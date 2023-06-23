import pytest
from app.app import GameMap,Tile
""" 

class GameMapTestCase(unittest.TestCase):
    def setUp(self):
        self.game_map = GameMap(5)
        
    def test_distance_calculation(self):
        # Test distance calculation
        distance = self.game_map.point_distance((0, 0), (3, 4))
        self.assertAlmostEqual(distance, 5.0)
    
    def test_get_neighbours_within_radius(self):

        # Call the get_neighbours method with a radius of 1
        neighbors = self.game_map.get_neighbours((2, 2), 1)
        
        # Assert that the center tile is not in the neighbors list
        self.assertNotIn(self.game_map.tiles[2][2], neighbors)
        
        # Assert that all neighboring tiles are in the neighbors list
        expected_neighbors = [
            self.game_map.tiles[1][2],
            self.game_map.tiles[3][2],
            self.game_map.tiles[2][1],
            self.game_map.tiles[2][3]
        ]
        for neighbor in expected_neighbors:
            self.assertIn(neighbor, neighbors)
    
    def test_out_of_bounds(self):
        # Test out_of_bounds method with valid and invalid coordinates
        self.assertTrue(self.game_map.out_of_bounds((-1, 0)))
        self.assertFalse(self.game_map.out_of_bounds((0, 0)))
        self.assertFalse(self.game_map.out_of_bounds((4, 4)))
        self.assertTrue(self.game_map.out_of_bounds((5, 5)))

 """
def test_get_neighbours_in_radius_1():
    # Create a game map of size 5x5
    game_map = GameMap(5)
    
    # Set a specific tile as the center tile
    center_tile = game_map.tiles[2][2] 
    
    # Call the get_neighbours method with a radius of 1
    neighbors = game_map.get_neighbours((2, 2), 1)
    
    # Assert that the center tile is not in the neighbors list
    assert center_tile not in neighbors
    
    # Assert that all neighboring tiles are in the neighbors list
    assert game_map.tiles[1][2] in neighbors
    assert game_map.tiles[3][2] in neighbors
    assert game_map.tiles[2][1] in neighbors
    assert game_map.tiles[2][3] in neighbors
    
    print("get_neighbours test passed!")



def test_get_neighbours_in_radius_1_and_a_half():
    # Create a game map of size 5x5
    game_map = GameMap(5)
    
    # Set a specific tile as the center tile
    center_tile = game_map.tiles[2][2] 
    
    # Call the get_neighbours method with a radius of 1.5
    neighbors = game_map.get_neighbours((2, 2), 1.5)

    # Assert that all neighboring tiles are in the neighbors list
    assert game_map.tiles[3][3] in neighbors
    assert game_map.tiles[1][3] in neighbors
    assert game_map.tiles[3][1] in neighbors
    assert game_map.tiles[1][1] in neighbors

    # Assert that all tiles in radius 2 are not in the neighbors list
    assert game_map.tiles[4][2] not in neighbors
    assert game_map.tiles[0][2] not in neighbors
    assert game_map.tiles[2][4] not in neighbors
    assert game_map.tiles[2][0] not in neighbors

    print("get_neighbours test passed!")

def test_get_neighbours_in_radius_1_and_a_half_on_0_0():
    # Create a game map of size 5x5
    game_map = GameMap(5)
    
    # Set a specific tile as the center tile
    center_pos = (0,0)
    
    # Call the get_neighbours method with a radius of 1.5
    neighbors = game_map.get_neighbours((center_pos), 1.5)

    # Assert that all neighboring tiles are in the neighbors list
    assert game_map.tiles[0][1] in neighbors
    assert game_map.tiles[1][0] in neighbors
    assert game_map.tiles[1][1] in neighbors

    assert len(neighbors) == 3
    print("get_neighbours test passed!")

def test_get_neighbours_in_radius_1_in_map_edge_should_have_3_neighbours():
    # Create a game map of size 5x5
    game_map = GameMap(5)
    
    # Set a specific tile as the center tile
    center_pos = (1,0)
    
    # Call the get_neighbours method with a radius of 1
    neighbors = game_map.get_neighbours((center_pos), 1)

    # Assert that all neighboring tiles are in the neighbors list
    assert game_map.tiles[0][0] in neighbors
    assert game_map.tiles[2][0] in neighbors
    assert game_map.tiles[1][1] in neighbors

    assert len(neighbors) == 3
    print("get_neighbours test passed!")
# Run the test
pytest.main()
