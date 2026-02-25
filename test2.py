import os
import shutil
import time
import sys

# Your Ship Art
ship = r"""
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

def animate_off_screen(art_string, speed=0.03):
    # 1. Get terminal dimensions
    columns, lines = shutil.get_terminal_size()
    
    art_lines = art_string.strip("\n").split("\n")
    # Calculate the width of the ship itself (the longest line)
    ship_width = max(len(line) for line in art_lines)
    
    # Vertical centering
    top_padding = (lines - len(art_lines)) // 2

    # 2. Loop until the margin equals the full width of the screen
    # This ensures even the back of the ship passes the right edge
    for x in range(columns):
        sys.stdout.write("\033[H\033[J") # Clear/Home
        sys.stdout.write("\n" * top_padding)
        
        margin = " " * x
        for line in art_lines:
            # We use slicing [:(columns - x)] to prevent the text 
            # from "wrapping" to the next line as it hits the wall
            display_line = line[:(columns - x)]
            sys.stdout.write(f"{margin}{display_line}\n")
        
        sys.stdout.flush()
        time.sleep(speed)

animate_off_screen(ship)