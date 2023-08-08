import pytest
from app.entities.unit import Unit

from app.utilities.coordinates import Coordinate
from unittest.mock import MagicMock, patch
from app.controllers.commandHandler import CommandHandler


@pytest.fixture
def command_handler():
    port = MagicMock()
    unit_handler = MagicMock()
    return CommandHandler(port, unit_handler)


@pytest.mark.parametrize(
    ["args", "unit_id", "direction"],
    [[["63", "8"], 63, (1, 0)], [["67", "1"], 67, (-1, -1)]],
)
def test_call_to_walk_with_valid_arguments_should_call_unit_handler_walk(
    command_handler: CommandHandler, args, unit_id, direction
):
    coord = Coordinate(direction[0], direction[1])
    with patch.object(
        command_handler, "parse_direction", return_value=coord
    ) as mocker_parse_direction:
        command_handler.walk(args)
        mocker_parse_direction.assert_called_once_with(int(args[1]))
        command_handler.unit_handler.walk.assert_called_once_with(unit_id, coord)
