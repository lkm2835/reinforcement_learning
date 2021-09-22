import argparse
from argparse import RawTextHelpFormatter
from pathlib import Path

from parse_config import ConfigParser
from q_table import *
from q_network import *

def seed_setting(seed):
    np.random.seed(seed)
    pr.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


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