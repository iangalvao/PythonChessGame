from app.ports.commandPortInterface import CommandPortInterface
from app.router.router import RouterInterface
import threading
import queue


# Implement the interface in a separate class
class CommandPort(CommandPortInterface):
    def __init__(self, router: RouterInterface):
        self.router = router

    def get_command(self):
        command, args = None
        line = self.get_line()

        if line:
            prompt = line.split()
            command = prompt[0]
            if len(prompt) > 1:
                args = prompt[1:]

        return (command, args)

    def get_line(self):
        if not self.queue.empty():
            input_line = self.queue.get().split(" ")
            return input_line
        return None

    def input_thread(self):
        while True:
            input_line = input("(pyCiv3)$ ")
            self.router.execute(input_line.split())

    def listen(self):
        # Create a queue for communication between threads

        # Start the input thread
        self.input_thread()


"""         input_thread = threading.Thread(target=self.input_thread, args=(self,))
        input_thread.daemon = (
            True  # Set the thread as a daemon so it exits when the main program ends
        )
        input_thread.start() """
