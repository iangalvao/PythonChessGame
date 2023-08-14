class Match:
    def __init__(self, players) -> None:
        self.turn = 0
        self.players = players
        self.n_players = len(players)
        self.active_player = 0
        self.units = {}

    def next_turn(self):
        self.active_player += 1
        self.active_player %= self.n_players
