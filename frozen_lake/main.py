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
    board = FrozenLake()
    isGameDone = False

    while not isGameDone:
        board.printScreen()
        key = getChar()
        state = board.accept(key)
        if state == FrozenLakeState.Failed:
            isGameDone = True
            print("\nFailed")
        elif state == FrozenLakeState.Arrived:
            isGameDone = True
            print("\nArrived")


