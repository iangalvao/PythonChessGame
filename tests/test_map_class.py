import pytest
from app.entities.gamemap import GameMap, Tile


@pytest.fixture
def game_map():
    return GameMap(5)


@pytest.mark.parametrize(
    "point_a, point_b, expected_result",
    [
        ((1, 1), (1, 2), 1),
        ((1, 1), (1, 1), 0),
        ((1, 1), (2, 1), 1),
        ((2, 1), (1, 1), 1),
        ((1, 2), (1, 1), 1),
        ((1, 1), (1, 2), 1),
        ((0, 0), (3, 3), 4.5),
        ((0, 0), (0, 4), 4),
        ((4, 4), (4, 0), 4),
        ((1, 1), (2, 2), 1.5),
    ],
)
def test_game_map_distance(game_map, point_a, point_b, expected_result):
    assert game_map.point_distance(point_a, point_b) == expected_result
    print("point_distance test passed!")


@pytest.mark.parametrize(
    "center, radius, expected_result",
    [
        # all 4 neighbors in 1 distance from center tile
        ((1, 1), 1, ((0, 1), (1, 0), (2, 1), (1, 2))),
        # all 4 neighbors in 1.5 distance from center tile
        ((1, 1), 1.5, ((2, 2), (0, 0), (0, 2), (2, 0))),
        # all 3 neighbors in 1.5 distance from a corner tile
        ((0, 0), 1.5, ((0, 1), (1, 0), (1, 1))),
        # all 3 neighbors in 1 distance from a edge tile
        ((1, 0), 1, ((0, 0), (2, 0), (1, 1))),
    ],
)
def test_get_neighbours_valid_inputs(game_map, center, radius, expected_result):
    neighbors = game_map.get_neighbours(center, radius)
    # center tile not in neighbors
    assert game_map.tiles[center[0]][center[1]] not in neighbors
    # expected tiles should be in neighbors
    for pos in expected_result:
        x, y = pos
        assert game_map.tiles[x][y] in neighbors
    print("get_neighbours test passed!")


# Run the test
pytest.main()