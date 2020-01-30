from typing import Tuple

import pygame

from .constants import MAPS


class Map:

    def __init__(self, win) -> None:
        self.platform_list = pygame.sprite.Group()
        self.win = win
        self.background = None

    def update(self) -> None:
        self.platform_list.update()
        
    def draw(self) -> None:
        self.win.fill((255, 255, 255))

        self.platform_list.draw(self.win)


class Platform(pygame.sprite.Sprite):

    def __init__(self, height, width) -> None:
        super(Platform, self).__init__()
        
        self.image = MAPS['haven']['arena'].convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.left = (width // 2) - (self.rect.size[0] // 2)
        self.rect.top = (height // 2) - (self.rect.size[1] // 2)


class Haven(Map):

    def __init__(self, win) -> None:
        super(Haven, self).__init__(win)

        arena = Platform(self.win.get_height(), self.win.get_width())
        self.platform_list.add(arena)
