from ports.commandPortInterface import CommandPortInterface
from controllers.commandHandlerInterface import CommandHandlerInterface
from app.use_cases.unit_handler import UnitHandlerInterface
from utilities.coordinates import Coordinate


class CommandHandler(CommandHandlerInterface):
    def __init__(self, port: CommandPortInterface, unit_handler: UnitHandlerInterface):
        self.port = port

    def execute(self):
        # Check requests
        # Instantitate the request object model
        command, args = self.port.get_command()
        if not command:
            return

        # Handle the request object
        if command == "quit":
            exit(0)
        elif command == "walk":
            # Check if the package conforms to the request ( can i pass the object entirely?)
            if len(args) == 2:
                self.walk(args)
        else:
            print("Comando não reconhecido.\nEnter a Command:")

    def walk(self, args):
        unit_id, direction = args
        direction = Coordinate(self.parse_direction(int(direction)))
        self.unit_handler.walk(unit_id, direction)

    def parse_direction(self, direction):
        dir = (0, 0)
        i = 0
        j = 1
        for directions in [[7, 8, 9], [3, 6, 9], [1, 2, 3], [1, 4, 7]]:
            if direction in directions:
                dir = (dir[0] + i, dir[1] + j)
            aux = j
            j = -i
            i = aux
        return dir
