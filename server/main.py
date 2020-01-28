import toml

from core.server import Server
from core.exceptions import MissingConfiguration

if __name__ == "__main__":
    try:
        config = toml.load('config.toml')['server']
    
    except FileNotFoundError:
        raise MissingConfiguration('config.toml is missing') from None

    except KeyError:
        raise MissingConfiguration(
            'server configuration section in config.toml is missing'
        ) from None

    else:
        Server(**config).run()
