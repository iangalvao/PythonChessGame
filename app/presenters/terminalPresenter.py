from app.presenters.presenterInterface import PresenterInterface


class TerminalPresenter(PresenterInterface):
    def __init__(self) -> None:
        super().__init__()

    def walk(self, unit_id, pos):
        print(f"Event: walk {unit_id} {pos}")

    def next_turn(self, turn_number):
        print(f"Starting turn {turn_number}")

    def show_error_message(self, s: str):
        print("Error:" + s)
