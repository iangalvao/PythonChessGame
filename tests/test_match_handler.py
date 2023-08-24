from unittest.mock import MagicMock, patch
import pytest
from app.entities.match import Match
from app.entities.player import Player
from app.use_cases.match_handler import MatchHandler


@pytest.fixture
def match_handler() -> MatchHandler:
    player = Player("civ")
    match = Match([player])
    presenter = MagicMock()
    return MatchHandler(match, presenter)


@patch("app.entities.match.Match.next_turn", return_value=None)
@patch("app.entities.match.Match.get_turn", return_value=1)
def test_call_to_next_turn_should_call_match_next_turn(
    match_get_turn_mocker, match_next_turn_mocker, match_handler: MatchHandler
):
    # Mock the helper_method to return a specific value
    with patch.object(
        match_handler, "start_turn", return_value=None
    ) as match_handler_start_turn_mocker:
        #ACTION
        match_handler.next_turn()
        # MatchHandler object's ASSERTS
        match_handler_start_turn_mocker.assert_called_once_with(match_handler.match.players[0]) # called with next player
        match_handler.presenter.next_turn.assert_called_once_with(1) # called with turn 1 (next turn)
        # children Match object's ASSERTS
        match_next_turn_mocker.assert_called_once_with()
        match_get_turn_mocker.assert_called_once_with()
