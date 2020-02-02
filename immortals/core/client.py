from typing import Tuple

import pygame
from connectIO import Client

from .playerdata import PlayerData
from .player import Player
from .map import Haven


class ImmortalsClient:

    def __init__(
        self, 
        width: int = 1920,
        height: int = 1080,
        ip: str = '127.0.0.1', 
        port: int = 5555
    ) -> None:
    
        print(width, height, ip, port)

        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((width, height))
        self.is_running = True

        self.height = height
        self.width = width

        pygame.display.set_caption('Immortals')

        self.player_count = 0

        self.network = Client(ip, port)
        self.network.connect()
        self.userdata = self.network.recieve()

        self.active_sprites = list()

    def update_active_sprites(self):
        for sprite in self.active_sprites:
            sprite.update()

    def draw_active_sprites(self):
        for sprite in self.active_sprites:
            self.win.blit(sprite.image, sprite.rect)

    def refresh(self, map_arena, playerdata: Tuple['Player']) -> None:

        if len(playerdata) > self.player_count:
            self.player_count += 1
            self.active_sprites.append(
                Player(
                    playerdata[-1].data,
                    self.height, self.width,
                    map_arena
                )
            )

        for i, _ in enumerate(self.active_sprites[1:], 1):
            try:
                self.active_sprites[i].set_data(playerdata[i - 1].data)

            except IndexError:
                self.active_sprites.pop(i)
                self.player_count -= 1

        if self.user.rect.right > self.width:
            self.user.rect.right = self.width

        if self.user.rect.left < 0:
             self.user.rect.left = 0

        self.update_active_sprites()
        map_arena.update()
        pygame.display.flip()

    def run(self) -> None:
        map_ = Haven(self.win)
        self.user = Player(*self.userdata.data, self.height, self.width, map_)
        self.active_sprites.append(self.user)

        while self.is_running:
            self.clock.tick(60)

            self.userdata.data = self.user.data

            self.network.send(self.userdata)
            playerdata = self.network.recieve()
            
            self.refresh(map_, playerdata)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a:
                        self.user.move_left()

                    if event.key == pygame.K_d:
                        self.user.move_right()

                    if event.key == pygame.K_SPACE:
                        self.user.jump()

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a and self.user.x_delta < 0:
                        self.user.stop()

                    if event.key == pygame.K_d and self.user.x_delta > 0:
                        self.user.stop()

            map_.draw()
            self.draw_active_sprites()

# http://programarcadegames.com/python_examples/show_file.php?file=platform_jumper.py
