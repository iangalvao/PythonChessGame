class Match:
    def __init__(self, players) -> None:
        self.turn = 0
        self.players = players
        self.active_player = None
        self.units = {}
