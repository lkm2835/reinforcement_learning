import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


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
    return