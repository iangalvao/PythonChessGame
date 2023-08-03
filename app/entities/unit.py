class Unit:
    def __init__(self, unit_id, player, type) -> None:
        self.id = unit_id
        self.type = type
        self.player = player
        self.pos = None
        self.tile = None
