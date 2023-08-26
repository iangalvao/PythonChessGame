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
    map = GameMap(8)
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
def test_call_to_move_should_call_getUnitById_getTileFromPos_checkMove_addUnitToTile_and_presenter_showEvent(
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
        Coordinate(8, 3),  # value equal to map size on x coordinate
        Coordinate(3, 8),  # value equal to map size on y coordinate
    ],
)
def test_call_to_getTileFromPos_with_to_out_of_bounds_position_should_raise_value_error(
    unit_handler, pos
):
    with pytest.raises(ValueError) as exc_info:
        unit_handler.getTileFromPos(pos)
    assert str(exc_info.value) == "Moving unit to position out of bounds!"


@patch("app.entities.tile.Tile.add_unit")
@patch("app.entities.tile.Tile.remove_unit")
def test_call_to_add_unit_to_tile_with_valid_unit_and_tile(
    tile_remove_unit_mocker,
    tile_add_unit_mocker,
    unit_handler: UnitHandler,
    start_pos: Coordinate,
    unit: Unit,
):
    # SETUP
    target_tile = unit_handler.map.tiles[start_pos.x][start_pos.y]

    unit_handler.add_unit_to_tile(unit, target_tile)

    assert unit.pos == target_tile.pos  # Should assing unit pos as target_tile pos
    assert unit.tile == target_tile  # Should assing unit tile as target_tile
    tile_add_unit_mocker.assert_called_once_with(unit)  # Should call new tile add_unit
    tile_remove_unit_mocker.assert_called_once_with(
        unit.id
    )  # Should call old tile remove unit


def test_call_to_check_moves_with_valid_move_for_each_unit_type_should_make_the_proper_call_to_unit_moves(
    unit_handler: UnitHandler, start_pos: Coordinate
):
    new_pos = Coordinate(0, 0)
    active_player = 0
    type_methods_dict = {
        "H": "horse_moves",
        "B": "bishop_moves",
        "T": "tower_moves",
        "K": "king_moves",
        "Q": "queen_moves",
        "P": "pawn_moves",
    }
    for unit_type, method in type_methods_dict.items():
        with patch.object(
            unit_handler, method, return_value=[new_pos]
        ) as unit_moves_mocker:
            unit_handler.check_move(unit_type, start_pos, new_pos, active_player)
            unit_moves_mocker.assert_called_once_with(start_pos, active_player)


def test_call_to_check_moves_with_invalid_move_for_each_unit_type_should_raise_value_error_after_proper_call_to_each_move_method(
    unit_handler: UnitHandler, start_pos: Coordinate
):
    valid_move = Coordinate(0, 0)
    wrong_pos = Coordinate(3, 3)
    active_player = 0
    type_methods_dict = {
        "H": "horse_moves",
        "B": "bishop_moves",
        "T": "tower_moves",
        "K": "king_moves",
        "Q": "queen_moves",
        "P": "pawn_moves",
    }
    for unit_type, method in type_methods_dict.items():
        with patch.object(
            unit_handler, method, return_value=[valid_move]
        ) as unit_moves_mocker:
            with pytest.raises(ValueError) as exc_info:
                unit_handler.check_move(unit_type, start_pos, wrong_pos, active_player)
            assert (
                str(exc_info.value)
                == f"Invalid move: {unit_type} from {start_pos} to {wrong_pos}"
            )
            unit_moves_mocker.assert_called_once_with(start_pos, active_player)


@pytest.mark.parametrize(
    "pos, expected_results",
    [
        ((0, 0), [(1, 2), (2, 1)]),
        ((1, 0), [(0, 2), (2, 2), (3, 1)]),
        ((7, 7), [(6, 5), (5, 6)]),
        ((5, 5), [(6, 7), (7, 6), (6, 3), (7, 4), (4, 7), (3, 6), (3, 4), (4, 3)]),
    ],
)
def test_horse_moves_should_return_all_valid_horse_moves(
    unit_handler: UnitHandler, pos, expected_results
):
    pos = Coordinate(pos[0], pos[1])

    moves = unit_handler.horse_moves(pos, 0)

    for res in expected_results:
        assert Coordinate(res[0], res[1]) in moves
    for move in moves:
        assert (move.x, move.y) in expected_results


# Run the test
pytest.main()
