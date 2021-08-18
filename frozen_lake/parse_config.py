import json

class ConfigParser:
    def __init__(self, config):
        self.config = config
        return

    @classmethod
    def from_args(cls, args):
        args = args.parse_args()
        msg_no_cfg = "Configuration file need to be specified. Add '-c config.json', for example."
        assert args.config is not None, msg_no_cfg

        cfg_fname = './' + args.config

        with open('./'+args.config, 'r') as json_file:
            config = json.load(json_file)
        return cls(config)

    def __getitem__(self, name):
        return self.config[name]