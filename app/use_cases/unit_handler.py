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
    def walk(self, unit_id: int, direction: Coordinate) -> None:
        if direction.x not in (-1, 0, 1) or direction.y not in (-1, 0, 1):
            raise ValueError(
                f"unit_handler.walk direction arg components should be -1, 0 or 1: {direction}"
            )

        # try:
        #    unit = self.getUnitByID(unit_id)
        #    new_pos = unit.pos + direction
        #    action = check_if_movable(tile, unit)
        #    if action == "move":
        #       self.move_unit(unit, new_pos)
        #    if action == "combat":
        #       self.attack(unit, new_pos)
        #    self.presenter.send_event(action + ...)
        # except ValueError as e:
        #   self.presenter.send_error_message(str(e))
        # except KeyError as e:
        #   self.presenter.send_error_message(str(e))

        try:
            unit = self.getUnitByID(unit_id)
            new_pos = unit.pos + direction

            self.move_unit(unit, new_pos)
            self.presenter.walk(unit_id, (new_pos.x, new_pos.y))

        except ValueError as e:
            self.presenter.show_error_message(str(e))

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

    """
        if self.map.out_of_bounds(pos):
            raise ValueError("Moving unit to position out of bounds!")
        if unit.pos == pos:
            raise ValueError("Moving unit to it's own position!") 
    """

    @typechecked
    def move_unit(self, unit: Unit, pos: Coordinate) -> None:
        if self.map.out_of_bounds(pos):
            raise ValueError("Moving unit to position out of bounds!")
        if unit.pos == pos:
            raise ValueError("Moving unit to it's own position!")
        new_tile = self.map.get_tile(pos)
        if self.check_move(unit.type, unit.pos, pos):
            self.add_unit_to_tile(unit, new_tile)

    @typechecked
    def getUnitByID(self, unit_id: str) -> Unit:
        if unit_id not in self.units.keys():
            raise ValueError("Could not locate requested unit.")
        return self.units[unit_id]

    @typechecked
    def add_unit_to_tile(self, unit: Unit, tile: Tile):
        unit.tile.remove_unit(unit.id)
        tile.add_unit(unit)
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
        return True
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

    def horse_moves(self, pos, player):
        moves = []
        for i in (0, 1):
            for j in (-1, 1):
                for k in (-1, 1):
                    move = pos + (
                        i * (pos.x + j * -1, pos.y + k * -2)
                        + ((i + 1) % 2) * (pos.y + k * -2, pos.x + j * -1)
                    )
                    moves.append(Coordinate(move))

        moves = filter(lambda x: not self.map.out_of_bounds(x), moves)
        moves = filter(lambda x: self.getTileFromPos(x).unit.player != player, moves)
        return moves
