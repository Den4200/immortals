import toml
import pygame

from core.client import ImmortalsClient
from core.exceptions import MissingConfiguration

if __name__ == "__main__":
    try:
        config = toml.load('config.toml')
        configs = {**config['resolution'], **config['server']}

    except FileNotFoundError:
        raise MissingConfiguration('config.toml is missing') from None

    except KeyError:
        raise MissingConfiguration(
            'some configurations in config.toml are missing'
        ) from None

    else:
        pygame.init()
        ImmortalsClient(**configs).run()
