import json

class ConfigParser:
    def __init__(self, config):
        self._config = config
        return

    @classmethod
    def from_args(cls, args):
        args = args.parse_args()
        msg_no_cfg = "Configuration file need to be specified. Add '-c config.json', for example."
        assert args.config is not None, msg_no_cfg

        cfg_fname = './' + args.config

        with open('./'+args.config, 'r') as json_file:
            config = json.load(json_file)
        
        if args.q_algorithm == 'Q_table':
            config = config['Q_table']
            if args.episodes != None:
                config['num_episodes'] = args.episodes
                config['default'] = False

            if args.learning_method != None:
                config['Q_learning_method'] = args.learning_method
                if config['Q_learning_method'] == 1 or config['Q_learning_method'] == 2:
                    config['default'] = False

            if args.discount_rate != None:
                config['discounted'] = args.discount_rate
                config['default'] = False
            
            if args.learning_rate != None:
                config['learning_rate'] = args.learning_rate
                config['default'] = False

            if args.slippery != None:
                if args.slippery.lower() in ('n', 'no', 'f', 'false'):
                    config['slippery'] = False
                    config['default'] = False

        elif args.q_algorithm == 'Q_network':
            config = config['Q_network']

        else:
            raise print("q_algorithm is not defined")  

        return cls(config)

    def __getitem__(self, name):
        return self.config[name]

    @property
    def config(self):
        return self._config