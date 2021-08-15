import sys
import tty
import termios
import numpy as np
import random as pr
import matplotlib.pyplot as plt
import math
import argparse
from argparse import RawTextHelpFormatter

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
    num_episodes = 2000
    discounted = 0.9
    learning_rate = 0.2
    Q_learning_method = 1
    slippery = True

    parser = argparse.ArgumentParser(description='Parameters', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-episodes', type=int, help='number of episodes for one game')
    parser.add_argument('-learning_method', type=int, help=
                            'choose Q_learning_method 1~3\n'
                            'method 1 : use learning_rate, discounted_reward\n'
                            'method 2 : use discounted_reward\n'
                            'method 3 : vanila')
    parser.add_argument('-discount', type=float, help='discount reward rate')
    parser.add_argument('-learning_rate', type=float, help='learning rate')
    parser.add_argument('-slippery', type=str, help='slippery')
    args = vars(parser.parse_args())
    
    is_default = True

    if args['episodes'] != None:
        num_episodes = args['episodes']
        is_default = False

    if args['learning_method'] != None:
        Q_learning_method = args['learning_method']
        if Q_learning_method == 2 or Q_learning_method == 3:
            is_default = False

    if args['discount'] != None:
        discounted = args['discount']
        is_default = False
    
    if args['learning_rate'] != None:
        learning_rate = args['learning_rate']
        is_default = False

    if args['slippery'] != None:
        if args['slippery'].lower() in ('n', 'no', 'f', 'false'):
            slippery = False
            is_default = False

    print("========================\n")
    print("DEFAULT     ->\t", is_default)
    print("num_episodes  :\t", num_episodes)
    print("discount_rate :\t", discounted)
    print("learning_rate :\t", learning_rate)
    print("slippery_mode :\t", slippery)
    print("\n========================\n")
    
    pad = ['W', 'S', 'D', 'A', 'Q']

    games = 36
    action_history = np.zeros([games, FrozenLake.env_y_, FrozenLake.env_x_], dtype = np.int32)
    Arrived_rate = np.zeros([games])

    for game in range(games):
        print("Games : ", game+1, "\n")
        Q = np.zeros([FrozenLake.env_y_, FrozenLake.env_x_, FrozenLake.action_n_])
        Arrived = 0
        for i in range(num_episodes):
            #print("episode : ", i + 1, "\n")
            environment = FrozenLake(is_slippery = slippery)
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
                
                if Q_learning_method == 1:
                    Q[y_][x_][action] = (1 - learning_rate) * Q[y_][x_][action] + learning_rate * (reward + discounted * np.max(Q[new_y_][new_x_][:]))
                elif Q_learning_method == 2:
                    Q[y_][x_][action] = reward + discounted * np.max(Q[new_y_][new_x_][:])
                elif Q_learning_method == 3:
                    Q[y_][x_][action] = reward + np.max(Q[new_y_][new_x_][:])
                else:
                    Q[y_][x_][action] = (1 - learning_rate) * Q[y_][x_][action] + learning_rate * (reward + discounted * np.max(Q[new_y_][new_x_][:]))

                is_game_done = done

            if environment.state == FrozenLakeState.Arrived:
                Arrived += 1
            action_history[game] += environment.getHistory()
        #print(Q, "\n")
        print(action_history[game], "\n")
        Arrived_rate[game] = Arrived / num_episodes * 100
        print("Arrived :  {0:0.2f}".format(Arrived_rate[game]), "%\n\n")
    heatmapShow(action_history, Arrived_rate, games)