from typeguard import typechecked
from app.ports.commandPortInterface import CommandPortInterface
from app.controllers.commandHandlerInterface import CommandHandlerInterface
from app.use_cases.unit_handler import UnitHandlerInterface
from app.utilities.coordinates import Coordinate


class CommandHandler(CommandHandlerInterface):
    def __init__(self, port: CommandPortInterface, unit_handler: UnitHandlerInterface):
        self.port = port
        self.unit_handler = unit_handler

    def walk(self, args):
        unit_id, direction = args
        unit_id = int(unit_id)
        direction = self.parse_direction(int(direction))
        self.unit_handler.walk(unit_id, direction)

    @typechecked
    def parse_direction(self, direction: int):
        if direction not in range(10) or direction == 5:
            raise ValueError("Invalid direction.")

        dir = (0, 0)
        i = 0
        j = 1
        for directions in [[7, 8, 9], [3, 6, 9], [1, 2, 3], [1, 4, 7]]:
            if direction in directions:
                dir = (dir[0] + i, dir[1] + j)
            aux = j
            j = -i
            i = aux
        return Coordinate(dir[0], dir[1])
