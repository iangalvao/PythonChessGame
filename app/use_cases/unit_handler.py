from typeguard import typechecked
from app.entities.unit import *
from app.entities.gamemap import GameMap, Tile
from abc import ABC, abstractmethod
from app.utilities.coordinates import Coordinate
from app.presenters.presenterInterface import PresenterInterface


class UnitHandlerInterface(ABC):
    @abstractmethod
    def walk(self, unit, direction):
        pass


class UnitHandler:
    @typechecked
    def __init__(
        self, gamemap: GameMap, units: dict, presenter: PresenterInterface
    ) -> None:
        self.map = gamemap
        self.units = units
        self.presenter = presenter

    @typechecked
    def move(self, unit_id: str, pos: Coordinate):
        try:
            new_tile = self.getTileFromPos(pos)
            unit = self.getUnitByID(unit_id)
            self.check_move(unit.type, unit.pos, pos)
            self.add_unit_to_tile(unit, new_tile)
            self.presenter.show_event("move", unit.pos, new_tile.pos)
        except ValueError as e:
            self.presenter.show_error_message(str(e))

    @typechecked
    def getUnitByID(self, unit_id: str) -> Unit:
        if unit_id not in self.units.keys():
            raise ValueError("Could not locate requested unit.")
        return self.units[unit_id]

    @typechecked
    def add_unit_to_tile(self, unit: Unit, tile: Tile):
        tile.add_unit(unit)
        unit.tile.remove_unit(unit.id)
        unit.tile = tile
        unit.pos = tile.pos

    @typechecked
    def getTileFromPos(self, pos: Coordinate):
        if self.map.out_of_bounds(pos):
            raise ValueError("Moving unit to position out of bounds!")
        return self.map.get_tile(pos)

    @typechecked
    def next_turn(self, unit: Unit):
        pass

    @typechecked
    def check_move(
        self, unit_type: str, unit_pos: Coordinate, new_pos: Coordinate, player: int
    ):
        if unit_type == "H":
            moves = self.horse_moves(unit_pos, player)
        elif unit_type == "T":
            moves = self.tower_moves(unit_pos, player)
        elif unit_type == "B":
            moves = self.bishop_moves(unit_pos, player)
        elif unit_type == "K":
            moves = self.king_moves(unit_pos, player)
        elif unit_type == "Q":
            moves = self.queen_moves(unit_pos, player)
        elif unit_type == "P":
            moves = self.pawn_moves(unit_pos, player)
        if new_pos not in moves:
            raise ValueError(f"Invalid move: {unit_type} from {unit_pos} to {new_pos}")

    def horse_moves(self, pos: Coordinate, player: int):
        moves = []
        for i in (0, 1):
            for j in (-1, 1):
                for k in (-1, 1):
                    move = (
                        pos
                        + i * Coordinate(j * -1, k * -2)
                        + ((i + 1) % 2) * Coordinate(j * -2, k * -1)
                    )

                    moves.append(move)

        moves = list(filter(lambda x: not self.map.out_of_bounds(x), moves))
        # moves = filter(lambda x: self.getTileFromPos(x).unit.player != player, moves) #SHould be a function itself.
        return moves

    def valid_moves(self, pos: Coordinate, player: int):
        # check if there are player units.
        # check if the move causes a xeque. (just by removing the unit from position it should be possible to know)
        # Optional: check if move in tile_list
        pass

    def tower_moves(self, unit_pos: Coordinate, player: int):
        axis_list = ((0, 1), (1, 0), (0, -1), (-1, 0))
        return self.unit_moves_from_axis_list(unit_pos, player, axis_list)

    def bishop_moves(self, unit_pos: Coordinate, player: int):
        axis_list = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        return self.unit_moves_from_axis_list(unit_pos, player, axis_list)

    def king_moves(unit_pos, player):
        pass

    def queen_moves(self, unit_pos: Coordinate, player: int):
        axis_list = (
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        )
        return self.unit_moves_from_axis_list(unit_pos, player, axis_list)

    def pawn_moves(unit_pos, player):
        pass

    def check_player_unit(self, pos, player):
        tile = self.getTileFromPos(pos)
        return tile.getUnit().player == player

    def unit_moves_on_axis(self, pos, axis, player):
        moves = []
        while not self.map.out_of_bounds(pos):
            pos += axis
            tile = self.getTileFromPos(pos)
            if tile.units:
                if tile.getUnit().player == player:
                    break
                else:
                    moves.append(pos)
                    break
            moves.append(pos)
        return moves

    def unit_moves_from_axis_list(self, pos, player, axis_list):
        moves = []
        for axis in axis_list:
            for move in self.unit_moves_on_axis(pos, axis, player):
                moves.append(move)
        return moves

    """ 
    @typechecked
    def check_xeque(self, player: int):
        threats = []
        for unit in self.check_enemy_on_axis_list(tower_axis):
            if unit.type in ["Q", "T"]:
                threats += 1
        for unit in self.check_enemy_on_axis_list(bishop_axis):
            if unit.type in ["Q", "B"]:
                threats += 1
        # same for horse and pawn
        pass """

    def check_enemy_on_axis(self, axis, pos, player):
        moves = self.unit_moves_on_axis
        last_pos = moves[-1]
        # check if there is a enemy there, return enemy or none
        pass

    def check_enemy_on_axis_list(self, axis, pos, player):
        # same from the above, but return a list of units
        pass

    # Should call check_check for checking the units that threatens the king.
    # If two or more threats, valid_kings_moves tells if the are any valid move at all.
    # If zero threats, then return false
    # If one threat, should call valid_king_moves. if return is non-empty return False
    # Else it should check for units that might kill or block.
    # Should call empty_tiles_in_axis and add the tile with the threat.
    # For each of those, try to get a unit to move to it. can_move_to_tile_list?
    """ def check_mate(self, player):
        if self.check_xeque(self, player) > 1:
            return self.king_moves(king, kingpos).isempty()
        elif self.check_xeque(self, player) == 1:
            if not self.king_moves(king, kingpos).isempty():
                return False
            for unit in player.units:
                if not self.unit_moves(unit, unitpos).isempty():
                    return False
        return True
 """


# before moving:
#  check movalbe
#  check in unit type moveset
#  check for player's units

# after moving:
# check xeque
#   check two xeques (from the first)
#   check xeque mate (using units and number of xeques)
#
