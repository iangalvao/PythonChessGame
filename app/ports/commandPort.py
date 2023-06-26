from ports.commandPortInterface import CommandPortInterface
from controllers.commandHandlerInterface import CommandHandlerInterface


# Implement the interface in a separate class
class CommandPort(CommandPortInterface):
    def __init__(self, input_queue, command_handler=CommandHandlerInterface):
        self.queue = input_queue
        self.command_handler = command_handler

    def get_commands(self):
        if not self.queue.empty():
            input_line = self.queue.get().split(" ")
            self.command_handler.parse_line(input_line)
