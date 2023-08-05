import pytest
from app.entities.unit import Unit
from app.use_cases.unit_handler import UnitHandler
from app.entities.gamemap import GameMap
from app.utilities.coordinates import Coordinate
from unittest.mock import MagicMock


@pytest.fixture
def start_pos():
    return Coordinate(0, 0)


@pytest.fixture
def unit_id():
    return 63


@pytest.fixture
def unit_handler(unit_id, start_pos):
    map = GameMap(5)
    presenter = MagicMock()
    unit = Unit(unit_id, "foo", 0)
    map.tiles[start_pos.x][start_pos.y].add_unit(unit)
    return UnitHandler(map, {unit_id: unit}, presenter)


@pytest.mark.parametrize(
    "pos",
    [Coordinate(1, 1), Coordinate(2, 3), Coordinate(4, 4)],
)
def test_move_unit_to_valid_pos(unit_handler, unit_id, pos):
    unit = unit_handler.units[63]
    old_tile = unit_handler.map.tiles[unit.pos.x][unit.pos.y]
    new_tile = unit_handler.map.tiles[pos.x][pos.y]

    unit_handler.move_unit(unit, pos)

    assert unit_id in new_tile.units.keys()
    assert unit_id not in old_tile.units.keys()
    assert new_tile.units[unit_id] == unit
    assert unit.tile == new_tile
    assert unit.pos == pos


@pytest.mark.parametrize(
    "pos",
    [
        Coordinate(-1, 1),
        Coordinate(1, -1),
        Coordinate(5, 3),
        Coordinate(3, 5),
    ],
)
def test_move_unit_to_out_of_bounds_pos(unit_handler, unit_id, pos):
    unit = unit_handler.units[unit_id]
    old_tile = unit_handler.map.tiles[unit.pos.x][unit.pos.y]

    with pytest.raises(ValueError) as exc_info:
        unit_handler.move_unit(unit, pos)
    assert str(exc_info.value) == "Moving unit to position out of bounds!"

    assert unit_id in old_tile.units.keys()
    assert old_tile.units[unit_id] == unit
    assert unit.tile == old_tile
    assert unit.pos == old_tile.pos


def test_move_unit_to_its_own_tile_should_raise_value_error(unit_handler, unit_id):
    unit = unit_handler.units[unit_id]
    old_tile = unit_handler.map.tiles[unit.pos.x][unit.pos.y]

    with pytest.raises(ValueError) as exc_info:
        unit_handler.move_unit(unit, old_tile.pos)
    assert str(exc_info.value) == "Moving unit to it's own position!"

    assert unit_id in old_tile.units.keys()
    assert old_tile.units[unit_id] == unit
    assert unit.tile == old_tile
    assert unit.pos == old_tile.pos


@pytest.mark.parametrize("pos", [(0, 1), (1, 0), (1, 1)])
def test_walk_handler_calls_presenter_with_correct_args(unit_handler, unit_id, pos):
    coord = Coordinate(pos[0], pos[1])
    unit_handler.walk(unit_id, coord)
    unit_handler.presenter.walk.assert_called_once_with(unit_id, pos)


# Run the test
pytest.main()
