import pytest
from app.entities.gamemap import GameMap, Tile
from app.utilities.coordinates import Coordinate


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
    assert (
        game_map.point_distance(
            Coordinate(point_a[0], point_a[1]), Coordinate(point_b[0], point_b[1])
        )
        == expected_result
    )
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
    center = Coordinate(center[0], center[1])
    neighbors = game_map.get_neighbours(center, radius)

    assert game_map.get_tile(center) not in neighbors

    # expected tiles should be in neighbors
    for pos in expected_result:
        x, y = pos
        coord = Coordinate(x, y)
        assert game_map.get_tile(coord) in neighbors
    print("get_neighbours test passed!")


# Run the test
pytest.main()
