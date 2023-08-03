from presenterInterface import PresenterInterface


class TerminalPresenter(PresenterInterface):
    def __init__(self) -> None:
        super().__init__()

    def walk(self, unit_id, pos):
        print(f"Event: walk {unit_id} {pos}")
