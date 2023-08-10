from app.ports.commandPortInterface import CommandPortInterface


class Router:
    def __init__(self, port: CommandPortInterface, controller) -> None:
        self.port = port
        self.controller = controller

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
                self.controller.walk(args)
        else:
            print("Comando não reconhecido.\nEnter a Command:")
