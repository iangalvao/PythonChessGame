import pytest
from app.entities.unit import Unit
from app.entities.tile import Tile
from app.entities.gamemap import GameMap
from app.utilities.coordinates import Coordinate


@pytest.fixture
def unit_id():
    return 63


@pytest.fixture
def unit(unit_id):
    return Unit(unit_id, 0, "foo")


@pytest.fixture
def gamemap():
    return GameMap(5)


def test_add_unit_to_valid_tile(gamemap, unit, unit_id):
    tile = gamemap.tiles[2][2]

    tile.add_unit(unit)

    assert unit_id in tile.units.keys()
    assert tile.units[unit_id] == unit
    assert unit.tile == tile
    assert unit.pos == tile.pos


# Run the test
pytest.main()
