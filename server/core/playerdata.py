from typing import Tuple

import pygame


class PlayerData:

    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        color: Tuple[int, int, int]
    ) -> None:

        self.data = (
            x, y,
            width, height,
            color
        )
