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
        
        self.height = height
        self.width = width
        self.color = color

        self.screen_height = screen_height
        self.screen_width = screen_width

        self.x_delta = 0
        self.y_delta = 0

        self.map_arena = map_arena

        self.data = [
            self.rect.x, self.rect.y,
            width, height,
            color
        ]

    def update(self) -> None:
        self.calculate_gravity()

        # X axis
        self.rect.x += self.x_delta

        collided = pygame.sprite.spritecollide(self, self.map_arena.platform_list, False)
        for c in collided:

            if self.x_delta > 0:
                self.rect.right = c.rect.left
            elif self.x_delta < 0:
                self.rect.left = c.rect.right

        # Y axis
        self.rect.y += self.y_delta

        collided = pygame.sprite.spritecollide(self, self.map_arena.platform_list, False)
        for c in collided:

            if self.y_delta > 0:
                self.rect.bottom = c.rect.top
            elif self.y_delta < 0:
                self.rect.top = c.rect.bottom

        self.data = [
            self.rect.x, self.rect.y,
            self.width, self.height,
            self.color
        ]

    def calculate_gravity(self) -> None:
        if self.y_delta == 0:
            self.y_delta = 1
        else:
            self.y_delta += 0.25

        if (
            self.rect.y >= (self.screen_height - self.rect.height)
            and self.y_delta >= 0
        ):
            self.y_delta = 0
            self.rect.y = self.screen_height - self.rect.height
    
    def jump(self) -> None:
        self.rect.y += 1
        collided = pygame.sprite.spritecollide(self, self.map_arena.platform_list, False)
        self.rect.y -= 1

        if len(collided) > 0 or self.rect.bottom >= self.screen_height:
            self.y_delta = -7.5

    def move_left(self) -> None:
        self.x_delta = -6

    def move_right(self) -> None:
        self.x_delta = 6

    def stop(self) -> None:
        self.x_delta = 0
