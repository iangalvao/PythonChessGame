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


@pytest.mark.parametrize("turn, next_turn", [(0, 1), (1, 2), (3, 4)])
def test_call_to_next_turn_with_last_player_as_active_player_should_increment_turn(
    match: Match, turn: int, next_turn: int
):
    # SETUP: set last player as active_player.
    match.active_player = len(match.players) - 1
    match.turn = turn

    # ACTION
    match.next_turn()

    # ASSERT
    assert match.turn == next_turn


@pytest.mark.parametrize("turn", [0, 1, 3])
def test_call_to_next_turn_with_active_player_other_than_the_last_should__not_increment_turn(
    match: Match, turn: int
):
    # SETUP: first player is active_player in the prop match.
    match.turn = turn

    # ACTION
    match.next_turn()

    # ASSERT
    assert match.turn == turn
