import sys
import math
from time import sleep
import numpy as np
import os
import random
import threading
import shutil
#upgrades we want for the game: speed, pressure, hp 
player = str(input("Enter ID Diver: "))
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
ocean_size_c = shutil.get_terminal_size().columns // 3 # //3 because each cell "[#]" is 3 chars wide
runs = 0
#Classes
class Entity:
    def __init__(self, name, health, damage):
        """Creates an entity."""
        self.entity_name = str(name)
        print(self.entity_name)
        self.entity_health = health
        print(self.entity_health)
        self.entity_damage = damage
        print(self.entity_damage)
        
class Chunk:
    def __init__(self, generation):
        if generation == 0: generation = 1
        generation = abs(generation)
        val = 1 / (1 + np.exp(-np.clip(generation, -500, 500))) * np.sqrt(1 / generation)
        self.seed = int(str(val).replace(".", "")[2:10])
    
    def seed_gen(self):
        tx = int(self.seed % ocean_size_c)
        ty = int((self.seed // 7) % ocean_size_r)
        return tx, ty
        
seed = Chunk(random.randint(0,19))
treasure_x, treasure_y = seed.seed_gen()
#Functions
def clear_terminal():
    # Check the operating system name
    if os.name == 'nt':
        # Command for Windows
        _ = os.system('cls')
    else:
        # Command for Linux, macOS, etc. ('posix' is a common value)
        _ = os.system('clear')
def draw_grid():
    clear_terminal()
     
    for r in range(ocean_size_r):
        row_str = ""
        for c in range(ocean_size_c):
            if r == player_y and c == player_x:
                row_str += f"{blue}[{red}X{blue}]{white}"
            elif r == treasure_y and c == treasure_x:
                row_str += f"{blue}[{gold}T{blue}]{white}"
            else:
                row_str += f"{blue}[#]{white}"
        print(row_str)
    print(f"{doubloons} Doubloons")
    print(f"{current_depth} Depth")
        
def clear():
    print("/033c", end="")
    sleep(0.5)

def Settings():
    """Used for settings in the menu"""
    print("Settings selected")
    #Settings options here
    
def Info():
    """Used for info in the menu"""
    print("Info selected: Here it is.")
    print(f"Player Name: {player}")
    print(f"Player HP: {player_hp}")
    print(f"Current Doubloons: {doubloons}")
    #More Info?
def shop():
    shop = True
    while shop == True:
        shop_selection = str(input("what would you like to buy?: ")).upper()
        if shop_selection == "UPGRADES":
            stat = str(input("Which stat would you like to upgrade? (health, maxpressure, speed): ")).lower()
            Upgrade(stat, 10, 5)
            print("Upgrade Successful")
            sleep(0.5)
            shop = False
        elif shop_selection == "CONSUMABLES":
            consumables_shop()
            print("Consumable Collected")
            sleep(0.5)
            shop =  False
        else:
            print("Invalid Option (Upgrades or Consumables)") 
def Upgrade(stat, amount, cost):
    global player_hp, player_max_pressure, player_speed, doubloons
    if stat == "health":
        if doubloons >= cost:
            player_hp += amount
            doubloons -= cost
    elif stat == "maxpressure":
        if doubloons >= cost:
            player_max_pressure += amount
            doubloons -= cost
    elif stat == "speed":
        if doubloons >= cost:
            player_speed += amount
            doubloons -= cost
    else:
        print("Unknown Upgrade")
def consumables_shop():
    pass

def Dive():
    global player_x, player_y, treasure_x, treasure_y, doubloons, current_depth
    
    print("DIVE Selected: Preparing to Dive")
    sleep(1) 
    
    while True:
        draw_grid()
        move = input("> ").lower()
        if move == 'q':
            break

        if move == 'u':
            shop()

        if move == 'wswsadadba':
            doubloons += 1000000000000000
            
        for char in move:
            if char == 'w': 
                # Prevents going below 0
                if player_y > 0:
                    player_y -= 1
                elif current_depth > 0: # If at top of grid but not surface
                    player_y = ocean_size_r - 1
                    current_depth -= 1

            elif char == 's': 
                # Prevents going beyond the bottom row (ocean_size_r - 1)
                if player_y < ocean_size_r - 1:
                    player_y += 1
                else: # If at the bottom, move to next depth
                    player_y = 0
                    current_depth += 1

            elif char == 'a': 
                # Stops at the far left (0)
                player_x = max(0, player_x - 1)

            elif char == 'd': 
                # Stops at the far right (ocean_size_c - 1)
                player_x = min(ocean_size_c - 1, player_x + 1)
            
            if player_x == treasure_x and player_y == treasure_y:
                doubloons += 5
                if seed.seed % 3 == 0: seed.seed += 1233
                else: seed.seed -= 1233
                treasure_x, treasure_y = seed.seed_gen() 
                sleep(0.5)

            draw_grid() 
            sleep(0.3)
def pirate_ship():
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟⠀⠀⠀")
    print("⠀⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁⠀⠀⠀")
    print("⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇⠀⠀⠀")
    print("⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠⠀⠀")
    print("⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿⠀⠀⠀")
    print("⠀⠀⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧⠀⠀⠀")
    print("⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿⠀⠀")
    print("⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
def reset_cursor():
    # \033[H moves cursor to the top-left (Home)
    # \033[J clears everything from the cursor to the end of the screen
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()
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
        sleep(0.1)

def text_worker():
    global char
    """Updates the message string one char at a time."""
    global current_text
    for char in message:
        current_text += char
        sleep(0.1)

def renderer():
    
    global char
    """The 'Brain' that draws both things at the same time."""
    columns, lines = shutil.get_terminal_size()
    art_lines = ship_art.strip("\n").split("\n")
    
    while len(current_text) < len(message):
        sys.stdout.write("\033[H\033[J") # Clear screen
        
        # Draw Ship
        ship_padding = " " * current_margin
        for line in art_lines:
            sys.stdout.write(f"{ship_padding}{line[:columns-current_margin]}\n")
        
        # --- TEXT LOGIC ---
        # Split the current progress into lines
        lines_of_text = current_text.splitlines()
        
        # If there is text, only show the most recent line
        display_text = lines_of_text[-1] if lines_of_text else ""
        
        sys.stdout.write("\n" * 3) 
        sys.stdout.write(f" > {display_text}")
        
        sys.stdout.flush()
        if char == "\n":
            sleep(0.125)
        else:
            sleep(0.03)
        

# 2. Start all tasks together
def ship_animation():
    global current_text, current_margin
    current_text = ""
    current_margin = 0
    clear_terminal()
    thread1 = threading.Thread(target=ship_worker)
    thread2 = threading.Thread(target=text_worker)
    thread3 = threading.Thread(target=renderer)

    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for them to finish
    thread2.join()
    print("\n\n--- MISSION START ---")
def Welcome():
    Print("Welcome to ")
    

availible_buttons = ["DIVE", "SETTINGS", "INFO", "QUIT"]
current_button = None
print(availible_buttons)
while current_button != "QUIT":
    current_button = str(input("To select a button, type any of the above options: ")).upper()
    if current_button == "DIVE":
        ship_animation()
        Dive()
    elif current_button == "SHOP":
        shop()
    elif current_button == "SETTINGS":
        Settings()
    
    elif current_button == "INFO":
        Info()
    elif current_button == "QUIT":
        print("Exiting Game...")
        sys.exit()
    #elif current_button == "TEST":
        
    else:
        print("You didn't type in a known button.")