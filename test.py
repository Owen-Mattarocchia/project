import sys
import time
import threading
import shutil

# 1. Setup the Art and Message
ship_art = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢠⢿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⣠⣿⢻⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠉⢸⠚⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⢹⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣠⣾⣷⡀⠀⣼⣯⣆⡤⡀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠰⠛⠛⠿⣿⣿⣧⣄⡀⠀⠀⠀⠀⢸⡯⢩⣽⣥⣤⣸⣿⡿⣷⣷⣿⣷⣯⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠉⠻⣿⣶⠀⠀⣠⣾⣧⣼⣿⣿⣿⣿⣿⣿⣏⠉⠉⠙⠻⠿⡷⣤⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣶⠀⣠⣄⣀⣠⣮⣵⠼⢿⣁⣞⣻⣿⡜⠀⠀⣶⣶⡏⢈⠀⠀⣷⣶⣶⣶⣶⣶⣇⣀⣀⣀⡀⠀⢀⡀⠀
⠀⠀⣀⣠⢺⣯⣼⢀⣻⣿⣿⣿⣿⣭⣽⣽⣿⣿⣿⣿⣿⣷⣴⣤⣶⣤⣼⣻⣈⣀⡀⢀⠀⠀⠀⠈⠉⣭⡁⢈⠉⠁⠹⡆
⠀⠀⣻⣿⢺⣿⣿⠿⢶⣿⣿⣿⡿⠟⢻⡟⠉⠉⠉⠉⠉⠉⠉⠉⠉⣍⠉⠉⡍⣛⣃⣉⣄⣀⣀⣀⣤⣤⣤⣭⣶⣶⣶⡟
⠀⣠⣿⣿⣾⣿⣷⣤⣾⣿⣿⣿⣧⣴⣿⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀
⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀
⠀⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠀
"""

message = f"Welcome Player\n\
Your mission is to retrieve the artifacts lost in the Flor de la Mar sinking, \n\
In order to retrieve the artifacts, click s to go down, a to go left, d to go right, and w to go up, \n\
click enter to lock in your choice of movement.,"

# Shared variables for the "Camera" to render
current_margin = 0
current_text = ""

def ship_worker():
    """Moves the ship left to right."""
    global current_margin
    columns, _ = shutil.get_terminal_size()
    for x in range(columns):
        current_margin = x
        time.sleep(0.1)

def text_worker():
    """Updates the message string one char at a time."""
    global current_text
    for char in message:
        current_text += char
        time.sleep(0.1)

def renderer():
    """The 'Brain' that draws both things at the same time."""
    columns, lines = shutil.get_terminal_size()
    art_lines = ship_art.strip("\n").split("\n")
    
    # Run until the text is finished
    while len(current_text) < len(message):
        # Move cursor to top-left
        sys.stdout.write("\033[H\033[J")
        
        # Draw Ship
        ship_padding = " " * current_margin
        for line in art_lines:
            # Slice the line to prevent wrapping at the edge
            sys.stdout.write(f"{ship_padding}{line[:columns-current_margin]}\n")
        
        # Move to the bottom of the screen for the text
        sys.stdout.write("\n" * 3) 
        sys.stdout.write(f" > {current_text}")
        
        sys.stdout.flush()
        time.sleep(0.03)

# 2. Start all tasks together
thread1 = threading.Thread(target=ship_worker)
thread2 = threading.Thread(target=text_worker)
thread3 = threading.Thread(target=renderer)

thread1.start()
thread2.start()
thread3.start()

# Wait for them to finish
thread2.join()
print("\n\n--- MISSION START ---")