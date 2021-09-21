import numpy as np
import random as pr
import matplotlib.pyplot as plt
import argparse
import os
from argparse import RawTextHelpFormatter
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

from frozen_lake import *
from parse_config import ConfigParser


def seed_setting(seed):
    np.random.seed(seed)
    pr.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def heatmapShow(matrix, config, title, num_subplots = 1):
    fig = plt.figure(figsize=(10, 10))
    plt.subplots_adjust(bottom=0.1, left=0.001, right=0.999, top=0.90, hspace=0.75)
    plt.suptitle(config['algorithm'])

    ax = list()
    for i in range(1, num_subplots+1):
        ax.append(fig.add_subplot(int(np.sqrt(num_subplots)), int(np.sqrt(num_subplots)), i))
        plt.title("Arrived:{0:0.2f}".format(title[i-1]), size = 12)

    for i in range(num_subplots):
        ax[i].set_xticks(np.arange(4))
        ax[i].set_yticks(np.arange(4))
        ax[i].imshow(matrix[i], cmap='Reds')

    return


def increment_path(path):
    path_ = Path(path.split('/')[0])
    if not path_.exists():
        os.mkdir(path_)
    
    n = 0
    while True:
        path_ = Path(f"{path}{n}")
        if not path_.exists():
            print(f"mkdir {path_}")
            os.mkdir(path_)
            break
        elif path_.exists():
            n += 1
    
    return str(path_)


def rargmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return pr.choice(indices)


def Q_table(config):
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
        print(action_history[game], "\n")
        Arrived_rate[game] = Arrived / config['num_episodes'] * 100
        print("Arrived :  {0:0.2f}".format(Arrived_rate[game]), "%\n\n")
    heatmapShow(action_history, config, Arrived_rate, games)
    return

class QNModel(nn.Module):
    def __init__(self):
        super(QNModel, self).__init__()
        self.fc1     = nn.Linear(in_features=16, out_features=4)
        #self.fc2     = nn.Linear(in_features=8, out_features=4)

    def forward(self, x):
        x = self.fc1(x)
        #x = self.fc2(x)
        return x

def Q_network(config):
    pad = ['W', 'S', 'D', 'A', 'Q']

    games = 1
    action_history = np.zeros([games, FrozenLake.env_y_, FrozenLake.env_x_], dtype = np.int32)
    Arrived_rate = np.zeros([games])

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    for game in range(games):
        print("Games : ", game+1, "\n")
        Arrived = 0
        model = QNModel().to(device)
        criterion = nn.MSELoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        model.train()
        for i in range(config['num_episodes']):
            environment = FrozenLake(is_slippery = config['slippery'])
            is_game_done = False
            loss_all = 0
            while not is_game_done:
                y_, x_ = environment.getCurrYX()
                state = F.one_hot(torch.tensor(y_*4 + x_), 16).float().to(device)
                print(state)

                optimizer.zero_grad()

                Qs = model.forward(state)

                e = 1 / (i/500+1)
                if np.random.random() < e:
                    action = np.random.randint(4)
                else:
                    action = torch.argmax(Qs)
                
                new_y_, new_x_, reward, done = environment.accept(pad[action])
                if done:
                    Qs[action] = reward
                else:
                    state = torch.zeros(16)
                    state[new_y_*4 + new_x_] = 1
                    Qs1 = model.forward(state.to(device))
                    Qs[action] = reward + 0.99 * torch.max(Qs1)

                action = F.one_hot(torch.tensor(action), 4).float().to(device)
                loss = criterion(Qs, action)
                loss.backward()
                optimizer.step()

                loss_all += loss.item()
                is_game_done = done
            if i % 500 == 0:
                print("loss : ", loss_all)
            if environment.state == FrozenLakeState.Arrived:
                Arrived += 1
            action_history[game] += environment.getHistory()
        print(action_history[game], "\n")
        Arrived_rate[game] = Arrived / config['num_episodes'] * 100
        print("Arrived :  {0:0.2f}".format(Arrived_rate[game]), "%\n\n")
    heatmapShow(action_history, config, Arrived_rate, games)
    return


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Parameters', formatter_class=RawTextHelpFormatter)
    args.add_argument('-c', '--config', default=None, type=str, help='config file path (default: None')
    args.add_argument('-q', '--q_algorithm', default='Q_table', type=str, help='Q_table or Q_network')
    args.add_argument('-s', '--saved_dir', default='exp', type=str, help='saved directory saved/your_path')

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

    seed_setting(config['seed'])
    saved_path = increment_path(f"saved/{config['saved_dir']}")
    os.system(f"cp {config['fname']} {saved_path}")
    
    Q_table(config)
    #Q_network(config)
    plt.savefig(f'{saved_path}/result.png', dpi=300)