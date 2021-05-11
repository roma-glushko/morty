import sys

sys.path.append('../..')
sys.path.append('../../morty')

from morty.config import main, ConfigManager


@main(config_path='configs', config_name='basic_config')
def train(config: ConfigManager) -> None:
    # simply print out config file
    print(config)
    print(config.sgd.momentum)


if __name__ == "__main__":
    train()