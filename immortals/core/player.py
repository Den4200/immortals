from typing import Tuple

import pygame

from .playerdata import PlayerData


class Player(pygame.sprite.Sprite):

    def __init__(
        self, 
        x: int, y: int, 
        width: int, height: int, 
        color: Tuple[int, int, int],
        screen_height: int,
        screen_width: int,
        map_arena
    ) -> None:

        super(Player, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen_height = screen_height
        self.screen_width = screen_width

        self.x_delta = 0
        self.y_delta = 0

        self.map_arena = map_arena

    def update(self) -> None:
        self.calculate_gravity()

        self.rect.x += self.x_delta

        collided = pygame.sprite.collide_rect(self, self.map_arena)

        if collided:

            if self.y_delta > 0:
                self.rect.bottom = self.map_arena.rect.top

            elif self.y_delta < 0:
                self.rect.top = self.map_arena.rect.bottom

            self.y_delta = 0

    def calculate_gravity(self) -> None:
        if self.y_delta == 0:
            self.y_delta = 1
        else:
            self.y_delta += 0.35

        if (
            self.rect.y >= (self.screen_height - self.rect.height)
            and self.y_delta >= 0
        ):
            self.y_delta = 0
            self.rect.y = self.screen_height - self.rect.height
    
    def jump(self) -> None:
        self.rect.y += 2
        collided = pygame.sprite.collide_rect(self, self.map_arena)
        self.rect.y -= 2

        if self.rect.bottom >= self.screen_height or collided:
            self.y_delta = -10

    def move_left(self) -> None:
        self.x_delta = -6

    def move_right(self) -> None:
        self.x_delta = 6

    def stop(self) -> None:
        self.x_delta = 0
