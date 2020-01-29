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


    #     self.rect = (x, y, width, height)
    #     self.vel = 3

    #     self.is_jumping = False
    #     self.jump_offset = 0
    #     self.jump_height = 100

    # def init(self, arena_floor):
    #     self.arena_floor = arena_floor
    #     self.jump_offset = arena_floor * -1
    #     self.jump_height -= self.arena_floor

    # def draw(self, win):
    #     pygame.draw.rect(win, self.color, self.rect)

    # def move(self):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_a]:
    #         self.x -= self.vel

    #     if keys[pygame.K_d]:
    #         self.x += self.vel

    #     if keys[pygame.K_SPACE] and not self.is_jumping and self.jump_offset == self.arena_floor * -1:
    #         self.is_jumping = True

    #     self.check_jump()
    #     self.update()

    # def check_jump(self):
    #     if self.is_jumping:
    #         self.jump_offset += self.vel

    #         if self.jump_offset >= self.jump_height:
    #             self.is_jumping = False

    #     elif self.jump_offset > self.arena_floor * -1 and not self.is_jumping:
    #         self.jump_offset -= self.vel

    # def update(self):
    #     self.rect = (self.x, self.y - self.jump_offset, self.width, self.height)
