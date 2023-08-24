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
    def next_turn(self, unit: Unit):
        pass

    @typechecked
    def check_move(self, type, unit_pos, new_pos, player):
        return True
        if type == "H":
            return new_pos in self.horse_moves(unit_pos, player)
        elif type == "T":
            return new_pos in self.tower_moves(unit_pos, player)
        elif type == "B":
            return new_pos in self.bishop_moves(unit_pos, player)
        elif type == "K":
            return new_pos in self.king_moves(unit_pos, player)
        elif type == "Q":
            return new_pos in self.queen_moves(unit_pos, player)
        elif type == "P":
            return new_pos in self.pawn_moves(unit_pos, player)

    def horse_moves(self, pos, player):
        moves = []
        for i in (0, 1):
            for j in (-1, 1):
                for k in (-1, 1):
                    move = pos + (
                        i * (pos.x + j * -1, pos.y + k * -2)
                        + ((i + 1) % 2) * (pos.y + k * -2, pos.x + j * -1)
                    )
                    moves.append(move)

        moves = filter(self.map.out_of_bounds(), moves)
        moves = filter(has_player_units(player), moves)
        return moves
