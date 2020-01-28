from typing import Callable
from threading import Thread


def threaded(func: Callable) -> Callable:
    """
    A decorator that runs a function on
    a separate thread.
    """

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    return wrapper
