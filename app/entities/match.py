class Match:
    def __init__(self, players) -> None:
        self.turn = 0
        self.players = players
        self.n_players = len(players)
        self.active_player = 0
        self.units = {}

    def get_turn(self):
        return self.turn

    def next_turn(self):
        self.active_player += 1
        self.active_player %= self.n_players
        if self.active_player == 0:
            self.turn += 1
        # self.players[self.active_player].start_turn()

    def get_active_player(self):
        return self.players[self.active_player]
