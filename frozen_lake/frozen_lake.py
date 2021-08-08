from enum import Enum
import os

class FrozenLakeState(Enum):
    Running = 0
    Failed = 1
    Arrived = 2


class FrozenLake():
    def __init__(self):
        self.current_x = 1
        self.current_y = 1
        self.oScreen = [ ['O', 'O', 'O', 'O', 'O', 'O'],
                         ['O', 'S', 'F', 'F', 'F', 'O'],
                         ['O', 'F', 'H', 'F', 'H', 'O'],
                         ['O', 'F', 'F', 'F', 'H', 'O'],
                         ['O', 'H', 'F', 'F', 'G', 'O'],
                         ['O', 'O', 'O', 'O', 'O', 'O'] ]
        return

    def accept(self, key):
        self.state = FrozenLakeState.Running

        if key.upper() == 'Q':
            self.state = FrozenLakeState.Failed
        elif key.upper() == 'W':
            self.current_y -= 1
        elif key.upper() == 'S':
            self.current_y += 1
        elif key.upper() == 'D':
            self.current_x += 1
        elif key.upper() == 'A':
            self.current_x -= 1

        if self.oScreen[self.current_y][self.current_x] == 'H':
            self.state = FrozenLakeState.Failed

        if self.oScreen[self.current_y][self.current_x] == 'G':
            self.state = FrozenLakeState.Arrived

        if self.oScreen[self.current_y][self.current_x] == 'O':
            if key.upper() == 'W':
                self.current_y += 1
            elif key.upper() == 'S':
                self.current_y -= 1
            elif key.upper() == 'D':
                self.current_x -= 1
            elif key.upper() == 'A':
                self.current_x += 1

        return self.state

    def printScreen(self):
        os.system('clear')
        for i in range(1, len(self.oScreen)-1):
            for j in range(1, len(self.oScreen[i])-1):
                if i == self.current_y and j == self.current_x:
                    print("\x1b[41m" + self.oScreen[i][j] + "\x1b[40m", end = " ")
                else:
                    print(self.oScreen[i][j], end = " ")
            print()
        return
            