import json
import numpy as np
import random as pr
import matplotlib.pyplot as plt
import math
import argparse
from argparse import RawTextHelpFormatter

from frozen_lake import *
from parse_config import ConfigParser

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

def main(config):
    pad = ['W', 'S', 'D', 'A', 'Q']

    games = 36
    action_history = np.zeros([games, FrozenLake.env_y_, FrozenLake.env_x_], dtype = np.int32)
    Arrived_rate = np.zeros([games])

    for game in range(games):
        print("Games : ", game+1, "\n")
        Q = np.zeros([FrozenLake.env_y_, FrozenLake.env_x_, FrozenLake.action_n_])
        Arrived = 0
        for i in range(config['num_episodes']):
            environment = FrozenLake(is_slippery = config['slippery'])
            is_game_done = False
            while not is_game_done:                
                y_, x_ = environment.getCurrYX()
                e = 1 / (i + 1)
                if np.random.random() < e:
                    action = np.random.randint(4)
                else:
                    action = rargmax(Q[y_][x_][:].reshape(environment.action_n_))
                new_y_, new_x_, reward, done = environment.accept(pad[action])
                
                if config['Q_learning_method'] == 1:
                    Q[y_][x_][action] = reward + np.max(Q[new_y_][new_x_][:])
                elif config['Q_learning_method'] == 2:
                    Q[y_][x_][action] = reward + config['discounted'] * np.max(Q[new_y_][new_x_][:])
                elif config['Q_learning_method'] == 3:
                    Q[y_][x_][action] = (1 - config['learning_rate']) * Q[y_][x_][action] + config['learning_rate'] * (reward + config['discounted'] * np.max(Q[new_y_][new_x_][:]))
                else:
                    Q[y_][x_][action] = (1 - config['learning_rate']) * Q[y_][x_][action] + config['learning_rate'] * (reward + config['discounted'] * np.max(Q[new_y_][new_x_][:]))

                is_game_done = done

            if environment.state == FrozenLakeState.Arrived:
                Arrived += 1
            action_history[game] += environment.getHistory()
        #print(Q, "\n")
        print(action_history[game], "\n")
        Arrived_rate[game] = Arrived / config['num_episodes'] * 100
        print("Arrived :  {0:0.2f}".format(Arrived_rate[game]), "%\n\n")
    heatmapShow(action_history, Arrived_rate, games)
    return

if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Parameters', formatter_class=RawTextHelpFormatter)
    args.add_argument('-c', '--config', default=None, type=str, help='config file path (default: None')
        
    args.add_argument('-ep', '--episodes', type=int, help='number of episodes for one game')
    args.add_argument('-lm', '--learning_method', type=int, help=
                            'choose Q_learning_method 1~3\n'
                            'method 1 : use learning_rate, discounted_reward\n'
                            'method 2 : use discounted_reward\n'
                            'method 3 : vanila')
    args.add_argument('-dr', '--discount_rate', type=float, help='discount reward rate')
    args.add_argument('-lr', '--learning_rate', type=float, help='learning rate')
    args.add_argument('-sl','--slippery', type=str, help='slippery')

    config = ConfigParser.from_args(args)

    print("========================\n")
    print("cfg_fname      :\t", config['fname'])
    print("DEFAULT       ->\t", config['default'])
    print("learning_method:\t", config['Q_learning_method'])
    print("num_episodes   :\t", config['num_episodes'])
    print("discount_rate  :\t", config['discounted'])
    print("learning_rate  :\t", config['learning_rate'])
    print("slippery_mode  :\t", config['slippery'])
    print("\n========================\n")
    
    main(config)    