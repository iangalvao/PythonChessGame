import pytest
from app.entities.unit import Unit
from app.use_cases.unit_handler import UnitHandler
from app.entities.gamemap import GameMap
from app.utilities.coordinates import Coordinate
from unittest.mock import MagicMock, patch


@pytest.fixture
def start_pos():
    return Coordinate(2, 2)


@pytest.fixture
def unit_id():
    return "KH"


@pytest.fixture
def unit(unit_id):
    return Unit(unit_id, 0, "H")


@pytest.fixture
def unit_handler(unit_id, unit, start_pos):
    map = GameMap(5)
    presenter = MagicMock()
    map.tiles[start_pos.x][start_pos.y].add_unit(unit)
    unit.pos = start_pos
    unit.tile = map.tiles[start_pos.x][start_pos.y]
    units = {unit_id: unit}
    return UnitHandler(map, units, presenter)


@pytest.mark.parametrize(
    "pos",
    [(4, 3), (3, 4), (1, 3)],
)
@patch("app.use_cases.unit_handler.UnitHandler.add_unit_to_tile", return_value=None)
@patch("app.use_cases.unit_handler.UnitHandler.check_move", return_value=True)
def test_call_to_moveUnit_should_call_getUnitById_getTileFromPos_checkMove_addUnitToTile_and_presenter_showEvent(
    check_moves_mocker, add_unit_to_tile_mocker, pos, unit_handler: UnitHandler, unit_id
):
    # SETUP
    unit = unit_handler.units[unit_id]
    pos = Coordinate(pos[0], pos[1])
    old_tile = unit_handler.map.tiles[unit.pos.x][unit.pos.y]
    new_tile = unit_handler.map.tiles[pos.x][pos.y]

    # Mock the unit_handler's methods that should return the objects created on setup above.
    with patch.object(
        unit_handler, "getTileFromPos", return_value=new_tile
    ) as getTile_mocker, patch.object(
        unit_handler, "getUnitByID", return_value=unit
    ) as getUnit_mocker:
        # ACTION
        unit_handler.move(unit_id, pos)

    # ASSERTS
    getTile_mocker.assert_called_once_with(pos)
    getUnit_mocker.assert_called_once_with(unit_id)
    check_moves_mocker.assert_called_once_with(unit.type, old_tile.pos, new_tile.pos)
    add_unit_to_tile_mocker.assert_called_once_with(unit, new_tile)
    unit_handler.presenter.show_event.assert_called_once_with("move", unit.pos, pos)


@pytest.mark.parametrize(
    "pos",
    [
        Coordinate(-1, 1),  # negative value on x coordinate
        Coordinate(1, -1),  # negative value on y coordinate
        Coordinate(5, 3),  # value equal to map size on x coordinate
        Coordinate(3, 5),  # value equal to map size on y coordinate
    ],
)
def test_call_to_getTileFromPos_with_to_out_of_bounds_position_should_raise_value_error(
    unit_handler, pos
):
    with pytest.raises(ValueError) as exc_info:
        unit_handler.getTileFromPos(pos)
    assert str(exc_info.value) == "Moving unit to position out of bounds!"


def test_move_unit_to_its_own_tile_should_raise_value_error(unit_handler, unit_id):
    unit = unit_handler.units[unit_id]
    old_tile = unit.tile

    with pytest.raises(ValueError) as exc_info:
        unit_handler.move_unit(unit, old_tile.pos)
    assert str(exc_info.value) == "Moving unit to it's own position!"

    assert unit_id in old_tile.units.keys()
    assert old_tile.units[unit_id] == unit
    assert unit.tile == old_tile
    assert unit.pos == old_tile.pos


# change that. i'm testing 2 functions.
def test_add_unit_to_tile(unit_handler: UnitHandler, start_pos: Coordinate, unit: Unit):
    tile = unit_handler.map.tiles[start_pos.x][start_pos.y]

    unit_handler.add_unit_to_tile(unit, tile)

    assert unit.pos == tile.pos
    assert unit.tile == tile
    assert unit.id in tile.units.keys()
    assert tile.units[unit.id] == unit


# Run the test
pytest.main()
