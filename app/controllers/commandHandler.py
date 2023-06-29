from ports.commandPortInterface import CommandPortInterface
from controllers.commandHandlerInterface import CommandHandlerInterface


class CommandHandler(CommandHandlerInterface):
    def __init__(self, port: CommandPortInterface):
        self.port = port

    def execute(self):
        # Check requests
        prompt = self.port.get_line()
        if not prompt:
            return
        # Instantitate the request object model
        command, args = prompt

        # Handle the request object
        if command == "quit":
            exit(0)
        elif command == "move":
            # Check if the package conforms to the request ( can i pass the object entirely?)
            if len(args) == 2:
                print(f"move from point {args[0]} to {args[1]}")
        else:
            print("Comando não reconhecido.\nEnter a Command:")

    def move_unit(self, args):
        pass
