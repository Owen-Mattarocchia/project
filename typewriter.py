"""
import sys, time, os

message = "Welcome Player\n\
Your mission is to retrieve the artifacts lost in the Flor de la Mar sinking \n\
In order to retrieve the artifacts, click s to go down, a to go left, d to go right, and w to go up, \n\
click enter to lock in your choice of movement. \n\
Good luck solider,"
messages =""
def typewriter(message):
    global messages
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)
        messages = messages + char
os.system("cls") #CLEAR
typewriter(message)
"""
#"""
import multiprocessing
import time

def func1():
    print("func1: starting")
    time.sleep(2) # Simulate work
    print("func1: finishing")

def func2():
    print("func2: starting")
    time.sleep(2) # Simulate work
    print("func2: finishing")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=func1)
    p2 = multiprocessing.Process(target=func2)
    p1.start()
    p2.start()
    p1.join() # Wait for func1 to complete
    p2.join() # Wait for func2 to complete
    print("Both functions have finished execution.")
#"""