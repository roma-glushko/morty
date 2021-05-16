import sys

sys.path.append('../..')
sys.path.append('../../morty')

from morty.config import ComponentFactory, main, ConfigManager

scheduler_factory = ComponentFactory('scheduler')


@scheduler_factory.register('exponential_scheduler')
def get_exponential_scheduler():
    pass


@scheduler_factory.register('cosine_scheduler')
def get_cosine_scheduler():
    pass


@main(config_path='configs', config_name='basic_config')
def train(config: ConfigManager) -> None:
    # simply print out config file
    print(config)
    print(config.sgd.momentum)

    scheduler = scheduler_factory.get(config.scheduler)()
    print(scheduler_factory)

    for name, component in scheduler_factory:
        print(name)
        print(component)


if __name__ == "__main__":
    train()
