import sys
import tty
import termios
import numpy as np
import random as pr
import matplotlib.pyplot as plt
import math
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

def heatmapShow(matrix, title, num_subplots = 1, is_blocking=True, time=0):
    fig = plt.figure(figsize=(10, 10))
    plt.subplots_adjust(bottom=0.1, left=0.001, right=0.999, top=0.90, hspace=0.75)

    ax = list()
    for i in range(1, num_subplots+1):
        ax.append(fig.add_subplot(int(math.sqrt(num_subplots)), int(math.sqrt(num_subplots)), i))
        plt.title("Arrived:{0:0.2f}".format(title[i-1]), size = 12)

    for i in range(num_subplots):
        ax[i].set_xticks(np.arange(4))
        ax[i].set_yticks(np.arange(4))
        ax[i].imshow(matrix[i], cmap='Reds')

    #plt.colorbar()
    plt.show(block=is_blocking)
    plt.pause(time)
    plt.close()

def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return pr.choice(indices)

if __name__ == "__main__":
    pad = ['W', 'S', 'D', 'A', 'Q']

    games = 36
    history = np.zeros([games, FrozenLake.env_y_, FrozenLake.env_x_], dtype = np.int32)
    Arrived_rate = np.zeros([games])

    num_episodes = 10000
    discounted = 0.9
    learning_rate = 0.2
    for game in range(games):
        print("Games : ", game+1, "\n")
        Q = np.zeros([FrozenLake.env_y_, FrozenLake.env_x_, FrozenLake.action_n_])
        Arrived = 0
        for i in range(num_episodes):
            #print("episode : ", i + 1, "\n")
            environment = FrozenLake(is_slippery = True)
            is_game_done = False
            while not is_game_done:
                #board.printScreen()
                #action = getChar()
                #state = board.accept(action)
                
                y_, x_ = environment.getCurrYX()
                e = 1 / (i + 1)
                if np.random.random() < e:
                    action = np.random.randint(4)
                else:
                    action = rargmax(Q[y_][x_][:].reshape(environment.action_n_))
                new_y_, new_x_, reward, done = environment.accept(pad[action])
                
                Q[y_][x_][action] = (1 - learning_rate) * Q[y_][x_][action] + learning_rate * (reward + discounted * np.max(Q[new_y_][new_x_][:]))

                is_game_done = done

            if environment.state == FrozenLakeState.Arrived:
                Arrived += 1
            history[game] += environment.getHistory()
        #print(Q, "\n")
        print(history[game], "\n")
        Arrived_rate[game] = Arrived / num_episodes * 100
        print("Arrived :  {0:0.2f}".format(Arrived / num_episodes * 100), "%\n\n")
    heatmapShow(history, Arrived_rate, games)