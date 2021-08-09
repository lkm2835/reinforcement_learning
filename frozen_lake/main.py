import sys
import tty
import termios
from frozen_lake import *

def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    environment = FrozenLake()
    isGameDone = False

    while not isGameDone:
        environment.printScreen()
        action = getChar()
        state = environment.accept(action)
        if state != FrozenLakeState.Running:
            isGameDone = True

    environment.printScreen()
    if state == FrozenLakeState.Failed:
        print("\nFailed\n")
    elif state == FrozenLakeState.Arrived:
        print("\nArrived\n")
    print("Game Over!\n")