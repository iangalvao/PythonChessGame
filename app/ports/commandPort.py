from ports.commandPortInterface import CommandPortInterface
from controllers.commandHandlerInterface import CommandHandlerInterface
import threading
import queue


# Implement the interface in a separate class
class CommandPort(CommandPortInterface):
    def __init__(self, input_queue):
        self.queue = input_queue

    def get_line(self):
        if not self.queue.empty():
            input_line = self.queue.get().split(" ")
            command = input_line[0]
            return input_line

    def input_thread(self, x):
        while True:
            command = input("(pyCiv3)$ ")
            self.queue.put(command)

    def run_prompt(self):
        # Create a queue for communication between threads

        # Start the input thread
        input_thread = threading.Thread(target=self.input_thread, args=(self,))
        input_thread.daemon = (
            True  # Set the thread as a daemon so it exits when the main program ends
        )
        input_thread.start()
