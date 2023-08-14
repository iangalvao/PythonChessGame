from app.ports.commandPortInterface import CommandPortInterface
from app.controllers.commandHandlerInterface import CommandHandlerInterface

from abc import ABC, abstractmethod


# Define the interface using an abstract base class
class RouterInterface(ABC):
    @abstractmethod
    def execute(self):
        pass


class Router(RouterInterface):
    def __init__(self, controller: CommandHandlerInterface) -> None:
        self.controller = controller

    def execute(self, request):
        # Check requests
        # Instantitate the request object model

        command, args = request[0], request[1:]
        if not command:
            return
        # Handle the request object
        if command == "quit":
            exit(0)
        elif command == "walk":
            # Check if the package conforms to the request ( can i pass the object entirely?)
            if len(args) == 2:
                self.controller.walk(args)
        elif command == "next_turn":
            self.controller.next_turn()
        else:
            print("Comando não reconhecido.")
