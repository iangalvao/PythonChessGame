import pytest
from app.utilities.coordinates import Coordinate
from unittest.mock import MagicMock, patch
from app.controllers.commandHandler import CommandHandler


@pytest.fixture
def command_handler():
    port = MagicMock()
    unit_handler = MagicMock()
    return CommandHandler(port, unit_handler)


@pytest.mark.parametrize(
    ["unit_id", "unparsed_direction", "parsed_direction"],
    [[63, 8, (1, 0)], [67, 1, (-1, -1)]],
)
def test_call_to_walk_with_valid_arguments_should_call_unit_handler_walk(
    command_handler: CommandHandler, unit_id, unparsed_direction, parsed_direction
):
    # SETUP
    parsed_direction = Coordinate(parsed_direction[0], parsed_direction[1])
    args = [f"{unit_id}", f"{unparsed_direction}"]

    # Mocking command_handler.parse_direction
    with patch.object(
        command_handler, "parse_direction", return_value=parsed_direction
    ) as mocker_parse_direction:
        # ACTION
        command_handler.walk(args)
        # ASSERTS
        mocker_parse_direction.assert_called_once_with(unparsed_direction)
        command_handler.unit_handler.walk.assert_called_once_with(
            unit_id, parsed_direction
        )
