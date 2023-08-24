import pytest
from app.entities.unit import Unit
from app.entities.tile import Tile
from app.utilities.coordinates import Coordinate
from typeguard import TypeCheckError


@pytest.fixture
def unit_id():
    return "KH"


@pytest.fixture
def unit(unit_id):
    return Unit(unit_id, 0, "foo")


@pytest.fixture
def invalid_unit():
    return Unit(None, 0, "foo")


@pytest.fixture
def tile():
    return Tile(Coordinate(2, 2))


def test_add_unit_to_valid_tile(tile, unit, unit_id):
    tile.add_unit(unit)

    assert unit_id in tile.units.keys()
    assert tile.units[unit_id] == unit


def test_add_unit_with_invalid_unit_type_should_raise_type_error(tile):
    with pytest.raises(TypeCheckError) as exc_info:
        tile.add_unit("foo")
    assert (
        str(exc_info.value)
        == 'argument "unit" (str) is not an instance of app.entities.unit.Unit'
    )


def test_add_unit_with_invalid_unit_id_should_raise_type_error(tile, invalid_unit):
    with pytest.raises(AssertionError) as exc_info:
        tile.add_unit(invalid_unit)
    assert (
        str(exc_info.value)
        == "\"unit.id\" (<class 'NoneType'>) is not an instance of str"
    )


def test_remove_unit_with_invalid_unit_type_should_raise_type_error(tile):
    with pytest.raises(TypeCheckError) as exc_info:
        tile.remove_unit(10)
    assert str(exc_info.value) == 'argument "unit_id" (int) is not an instance of str'


# Run the test
pytest.main()
