from pygame.locals import *
import threading
import queue

from controllers.commandHandler import CommandHandler
from ports.commandPort import CommandPort


# Function to run in a separate thread for command line input
def input_thread(input_queue):
    while True:
        command = input("(pyCiv3)$ ")
        input_queue.put(command)


# Define the interface using an abstract base class


# Create a queue for communication between threads
input_queue = queue.Queue()

# Start the input thread
input_thread = threading.Thread(target=input_thread, args=(input_queue,))
input_thread.daemon = (
    True  # Set the thread as a daemon so it exits when the main program ends
)
input_thread.start()

command_handler = CommandHandler()
prompt_port = CommandPort(input_queue, command_handler)

while 1:
    prompt_port.get_commands()
