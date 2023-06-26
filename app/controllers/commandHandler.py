from ports.commandPortInterface import CommandPortInterface
from controllers.commandHandlerInterface import CommandHandlerInterface


class CommandHandler(CommandHandlerInterface):
    def __init__(self, command_port=CommandPortInterface):
        self.port = command_port

    def parse_line(self, input_line):
        command = input_line[0]
        args = []
        if len(input_line) > 1:
            args = input_line[1:]
        if command == "quit":
            exit(0)
        elif command == "move":
            if len(args) == 2:
                print(f"move from point {args[0]} to {args[1]}")
        else:
            print("Comando não reconhecido.\nEnter a Command:")
