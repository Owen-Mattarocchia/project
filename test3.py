import sys
import math
from time import sleep
import numpy as np
import os
import random
import threading
import shutil

# Initial Stats
player_hp = 10
player_max_pressure = 50
player_speed = 10
doubloons = 5

gold = "\033[33m"
red = "\033[31m"
white = "\033[0m"
blue = "\033[34m"

player_x, player_y = 0, 0
current_depth = 0 
ocean_size_r = 8
runs = 0

# --- Helper for Dynamic Width ---
def get_current_width():
    """Returns the current number of [ ] cells that fit in the terminal."""
    cols, _ = shutil.get_terminal_size()
    return max(1, cols // 3)  # Ensure at least 1 column exists

# --- Classes ---
class Entity:
    def __init__(self, name, health, damage):
        self.entity_name = str(name)
        self.entity_health = health
        self.entity_damage = damage
        
class Chunk:
    def __init__(self, generation):
        if generation == 0: generation = 1
        generation = abs(generation)
        val = 1 / (1 + np.exp(-np.clip(generation, -500, 500))) * np.sqrt(1 / generation)
        self.seed = int(str(val).replace(".", "")[2:10])
    
    def seed_gen(self, max_cols):
        """Now accepts the dynamic width of the ocean."""
        tx = int(self.seed % max_cols)
        ty = int((self.seed // 7) % ocean_size_r)
        return tx, ty
        
# Initialize seed and treasure
seed = Chunk(random.randint(0,19))
treasure_x, treasure_y = seed.seed_gen(get_current_width())

# --- Functions ---
def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write("\033[H\033[J")

def draw_grid():
    clear_terminal()
    current_w = get_current_width()
    
    for r in range(ocean_size_r):
        row_str = ""
        for c in range(current_w):
            if r == player_y and c == player_x:
                row_str += f"{blue}[{red}X{blue}]{white}"
            elif r == treasure_y and c == treasure_x:
                row_str += f"{blue}[{gold}T{blue}]{white}"
            else:
                row_str += f"{blue}[#]{white}"
        print(row_str)
    print(f"{gold}{doubloons} Doubloons{white} | Depth: {current_depth}")

def shop():
    # Simplistic shop logic for now
    print("Welcome to the shop!")
    sleep(1)

def Dive():
    global player_x, player_y, treasure_x, treasure_y, doubloons, current_depth
    
    print("DIVE Selected: Preparing to Dive")
    sleep(1) 
    
    while True:
        # Get width at the start of every frame
        current_w = get_current_width()
        
        # Safety: If terminal resized, keep player and treasure inside
        player_x = min(player_x, current_w - 1)
        treasure_x = min(treasure_x, current_w - 1)
        
        draw_grid()
        move = input("> ").lower()
        
        if move == 'q':
            break
        if move == 'u':
            shop()
        if move == 'wswsadadba':
            doubloons += 999999

        for char in move:
            if char == 'w': 
                if player_y > 0:
                    player_y -= 1
                elif current_depth > 0:
                    player_y = ocean_size_r - 1
                    current_depth -= 1
            elif char == 's': 
                if player_y < ocean_size_r - 1:
                    player_y += 1
                else:
                    player_y = 0
                    current_depth += 1
            elif char == 'a': 
                player_x = max(0, player_x - 1)
            elif char == 'd': 
                # Move based on current width
                player_x = min(current_w - 1, player_x + 1)
            
            # Check Treasure logic
            if player_x == treasure_x and player_y == treasure_y:
                doubloons += 5
                seed.seed = seed.seed + 1233 if seed.seed % 3 == 0 else seed.seed - 1233
                # Generate new treasure within current window bounds
                treasure_x, treasure_y = seed.seed_gen(get_current_width())
                draw_grid() # Visual update for collection
                sleep(0.2)

        draw_grid() 

# --- Animation/Intro Logic ---
ship_art = r"""
                      ⣀⡆
      ⣀            ⢠⢿⣷⡄
      ⣿            ⣠⣿⢻⢤
      ⣿            ⠉⢸⠚⠛
      ⢻            ⢹⣿
  ⣠⣤⡀            ⢸⣠⣾⣷⡀ ⣼⣯⣆⡤⡀  ⢀⡀
 ⠰⠛⠛⠿⣿⣿⣧⣄⡀      ⢸⡯⢩⣽⣥⣤⣸⣿⡿⣷⣷⣿⣷⣯⣧⡀
      ⠈⠁⠉⠻⣿⣶  ⣠⣾⣧⣼⣿⣿⣿⣿⣿⣿⣏⠉⠉⠙⠻⠿⡷⣤
  ⢀⣶ ⣠⣄⣀⣠⣮⣵⠼⢿⣁⣞⣻⣿⡜  ⣶⣶⡏⢈  ⣷⣶⣶⣶⣶⣶⣇⣀⣀⣀⡀ ⢀⡀
 ⣀⣠⢺⣯⣼⢀⣻⣿⣿⣿⣿⣭⣽⣽⣿⣿⣿⣿⣿⣷⣴⣤⣶⣤⣼⣻⣈⣀⡀⢀    ⠈⠉⣭⡁⢈⠉⠁⠹⡆
 ⣻⣿⢺⣿⣿⠿⢶⣿⣿⣿⡿⠟⢻⡟⠉⠉⠉⠉⠉⠉⠉⠉⠉⣍⠉⠉⡍⣛⣃⣉⣄⣀⣀⣀⣤⣤⣤⣭⣶⣶⣶⡟
⣠⣿⣿⣾⣿⣷⣤⣾⣿⣿⣿⣧⣴⣿⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
 ⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟
"""

message = "Welcome Player. Use WASD to move, ENTER to confirm. Retrieve the artifacts!"
current_text = ""
current_margin = 0

def ship_worker():
    global current_margin
    cols, _ = shutil.get_terminal_size()
    for x in range(cols // 2):
        current_margin = x
        sleep(0.05)

def text_worker():
    global current_text
    for char in message:
        current_text += char
        sleep(0.04)

def renderer():
    cols, _ = shutil.get_terminal_size()
    art_lines = ship_art.strip("\n").split("\n")
    while len(current_text) < len(message):
        sys.stdout.write("\033[H\033[J")
        padding = " " * current_margin
        for line in art_lines:
            sys.stdout.write(f"{padding}{line[:cols-current_margin]}\n")
        print(f"\n > {current_text}")
        sys.stdout.flush()
        sleep(0.05)

def ship_animation():
    global current_text, current_margin
    current_text, current_margin = "", 0
    t1 = threading.Thread(target=ship_worker)
    t2 = threading.Thread(target=text_worker)
    t3 = threading.Thread(target=renderer)
    t1.start(); t2.start(); t3.start()
    t2.join()
    print("\n\n--- MISSION START ---")

# --- Game Entry ---
player = input("Enter ID Diver: ")
available_buttons = ["DIVE", "SETTINGS", "INFO", "QUIT"]

while True:
    print(f"\nAvailable: {available_buttons}")
    choice = input("Choice: ").upper()
    if choice == "DIVE":
        ship_animation()
        Dive()
    elif choice == "QUIT":
        print("Goodbye!"); break
    elif choice == "INFO":
        print(f"Diver: {player} | Doubloons: {doubloons}")
    else:
        print("Invalid Selection.")