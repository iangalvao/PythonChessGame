import pytest
from app.entities.unit import Unit
from app.use_cases.unit_handler import UnitHandler
from app.entities.gamemap import GameMap
from app.utilities.coordinates import Coordinate
from unittest.mock import MagicMock, patch
from app.controllers.commandHandler import CommandHandler


@pytest.fixture
def command_handler():
    pass
