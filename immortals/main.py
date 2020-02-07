import toml
import arcade

from core.client import Immortals

if __name__ == "__main__":
    try:
        config = toml.load('immortals/config.toml')
        configs = {**config['resolution'], **config['server']}

    except FileNotFoundError:
        raise MissingConfiguration('config.toml is missing') from None

    except KeyError:
        raise MissingConfiguration(
            'some configurations in config.toml are missing'
        ) from None

    else:
        immortals = Immortals(**config['resolution'])
        arcade.run()
