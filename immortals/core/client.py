from typing import List

import pygame

from .network import Network
from .playerdata import PlayerData
from .player import Player
from .map import Haven


class Client:

    def __init__(
        self, 
        width: int = 1920,
        height: int = 1080,
        ip: str = '127.0.0.1', 
        port: int = 5555
    ) -> None:
    
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((width, height))
        self.is_running = True

        self.height = height
        self.width = width

        pygame.display.set_caption('Immortals')

        self.network = Network(ip, port)
        self.userdata = self.network.connect()
        self.active_sprites = pygame.sprite.Group()

    def refresh(self, map_arena, *playerdata: List['Player']) -> None:
        # self.user = Player(*user.data, self.height, self.width, map_arena)
        # self.active_sprites.add(self.user)

        # for pd in playerdata:
        #     self.active_sprites.add(Player(*pd.data, self.height, self.width, map_arena))

        if self.user.rect.right > self.width:
            self.user.rect.right = self.width

        if self.user.rect.left < 0:
             self.user.rect.left = 0

        self.active_sprites.update()
        map_arena.update()
        pygame.display.flip()

    def run(self) -> None:
        # self.user.init(self.win.get_height() // 2 - arena.rect.size[1])
        map_ = Haven(self.win)
        map_.draw()
        self.user = Player(*self.userdata.data, self.height, self.width, map_)
        self.active_sprites.add(self.user)

        while self.is_running:
            self.clock.tick(60)

            playerdata = self.network.send(self.userdata)
            self.refresh(map_, self.userdata, *playerdata)
            self.userdata.data = self.user.data

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

# http://programarcadegames.com/python_examples/show_file.php?file=platform_jumper.py
