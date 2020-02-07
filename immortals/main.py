import asyncio
import threading

import toml
import arcade

from core.client import Immortals


def thread_worker(window) -> None:
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(iomain(window, loop))
    loop.run_forever()

def main(*args, **kwargs):
    window = Immortals(*args, **kwargs)
    thread = threading.Thread(
        target=thread_worker, args=(window,), daemon=True
    )
    thread.start()
    arcade.run()


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
        main(**config['resolution'])
