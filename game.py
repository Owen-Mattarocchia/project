import sys
import math
from time import sleep
import numpy as np
import os
import random
import multiprocessing

#upgrades we want for the game: speed, pressure, 
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
ocean_size_r, ocean_size_c = 10, 60

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
        
def clear():
    print("/033c", end="")
    sleep(0.5)

def Dive():
    global player_x, player_y, treasure_x, treasure_y, doubloons
    
    print("DIVE Selected: Preparing to Dive")
    sleep(1) 
    
    while True:
        draw_grid()
        move = input("> ").lower()
        if move == 'q':
            break

        if move == 'wswsadadba':
            doubloons += 1000000000000000
            
        for char in move:
            if char == 'w': player_y = (player_y - 1) % ocean_size_r 
            elif char == 's': player_y = (player_y + 1) % ocean_size_r 
            elif char == 'a': player_x = (player_x - 1) % ocean_size_c 
            elif char == 'd': player_x = (player_x + 1) % ocean_size_c 
            
            if player_x == treasure_x and player_y == treasure_y:
                doubloons += 5
                if seed.seed % 3 == 0: seed.seed += 1233
                else: seed.seed -= 1233
                treasure_x, treasure_y = seed.seed_gen() 
                sleep(0.5)

            draw_grid() 
            sleep(0.3)

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
def research_ship_move():
    print("""
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠀⠀⠀
          
          """)
    sleep(0.5)
    clear_terminal()
    print("""
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    ⣀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
        ⠀⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠀⠀⠀                                    
          
          """)
    sleep(0.5)
    clear_terminal()
    print("""
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    ⣀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
                ⠀⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠀⠀⠀
          
          """)
def Welcome():
    pass
    

availible_buttons = ["DIVE", "SETTINGS", "INFO", "QUIT"]
current_button = None
print(availible_buttons)
while current_button != "QUIT":
    current_button = str(input("To select a button, type any of the above options: ")).upper()
    if current_button != "DIVE" and current_button != "SETTINGS" and current_button != "QUIT" and current_button != "INFO" and current_button != "TEST":
        print("You didn't type in a known button.")
    elif current_button == "DIVE":
        Dive()
    elif current_button == "SETTINGS":
        Settings()
    elif current_button == "INFO":
        Info()
    elif current_button == "QUIT":
        print("Exiting Game...")
        sys.exit()
    elif current_button == "TEST":
        research_ship_move()