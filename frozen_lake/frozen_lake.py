from enum import Enum
import numpy as np
import os

class FrozenLakeState(Enum):
    Running = 0
    Failed = 1
    Arrived = 2


class FrozenLake():
    env_x_ = 4
    env_y_ = 4
    action_n_ = 4
    def __init__(self):
        self.curr_x_ = 1
        self.curr_y_ = 1
        self.oScreen = [ ['O', 'O', 'O', 'O', 'O', 'O'],
                         ['O', 'S', 'F', 'F', 'F', 'O'],
                         ['O', 'F', 'H', 'F', 'H', 'O'],
                         ['O', 'F', 'F', 'F', 'H', 'O'],
                         ['O', 'H', 'F', 'F', 'G', 'O'],
                         ['O', 'O', 'O', 'O', 'O', 'O'] ]
        self.history = np.zeros([FrozenLake.env_y_+2,FrozenLake.env_y_+2], dtype = np.int32)
        self.history[self.curr_y_][self.curr_x_] += 1
        return

    def accept(self, action):
        self.state = FrozenLakeState.Running
        reward = 0
        is_game_done = False

        if action.upper() == 'Q':
            self.state = FrozenLakeState.Failed
        elif action.upper() == 'W':
            self.curr_y_ -= 1
        elif action.upper() == 'S':
            self.curr_y_ += 1
        elif action.upper() == 'D':
            self.curr_x_ += 1
        elif action.upper() == 'A':
            self.curr_x_ -= 1

        self.history[self.curr_y_][self.curr_x_] += 1

        if self.oScreen[self.curr_y_][self.curr_x_] == 'H':
            self.state = FrozenLakeState.Failed
            is_game_done = True

        if self.oScreen[self.curr_y_][self.curr_x_] == 'G':
            self.state = FrozenLakeState.Arrived
            reward = 1
            is_game_done = True

        if self.oScreen[self.curr_y_][self.curr_x_] == 'O':
            self.history[self.curr_y_][self.curr_x_] -= 1
            if action.upper() == 'W':
                self.curr_y_ += 1
            elif action.upper() == 'S':
                self.curr_y_ -= 1
            elif action.upper() == 'D':
                self.curr_x_ -= 1
            elif action.upper() == 'A':
                self.curr_x_ += 1

        return self.curr_y_-1, self.curr_x_-1, reward, is_game_done

    def getCurrYX(self):
        return self.curr_y_-1, self.curr_x_-1

    def getHistory(self):
        return self.history[1:-1, 1:-1]

    def printScreen(self):
        #os.system('clear')
        for i in range(1, len(self.oScreen)-1):
            for j in range(1, len(self.oScreen[i])-1):
                if i == self.curr_y_ and j == self.curr_x_:
                    print("\x1b[41m" + self.oScreen[i][j] + "\x1b[40m", end = " ")
                else:
                    print(self.oScreen[i][j], end = " ")
            print()
        print()
        return
    
    def printHistroy(self):
        for i in range(1, len(self.history)-1):
            for j in range(1, len(self.history[i])-1):
                print(self.history[i][j], end = " ")
            print()
        print()
            