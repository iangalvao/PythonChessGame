from typing import Tuple
import pytest
from app.entities.match import Match
from app.utilities.coordinates import Coordinate


@pytest.fixture
def match():
    return Match(["A", "B", "C", "D"])


@pytest.mark.parametrize("player, next_player", [(0, 1), (1, 2), (3, 0)])
def test_call_to_next_turn_should_increment_active_player(
    match: Match, player: int, next_player: int
):
    match.active_player = player
    match.next_turn()
    assert match.active_player == next_player
