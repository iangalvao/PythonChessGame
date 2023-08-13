import pytest
from unittest.mock import MagicMock, patch
from app.router.router import Router
from app.controllers.commandHandlerInterface import CommandHandlerInterface


@pytest.fixture
def router():
    commandHandler = MagicMock
    return Router(commandHandler())


def test_call_to_execute_with_walk_command(router):
    router.execute(["walk", "63", "6"])
    router.controller.walk.assert_called_once_with(["63", "6"])


def test_execute_quit_command_should_exit(router):
    # SETUP
    request = ["quit"]

    # Mocking exit function
    with patch("builtins.exit") as mocker_exit:
        # ACTION
        router.execute(request)
        # ASSERTS
        mocker_exit.assert_called_once_with(0)
