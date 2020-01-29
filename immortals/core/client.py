from typing import List

import pygame

from .network import Network
from .playerdata import PlayerData
from .player import Player
from .map import Platform, Map


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
        self.user = self.network.connect()

    def refresh(self, map_arena, *playerdata: List['Player']) -> None:
        self.win.fill((255,255,255))

        for pd in playerdata:
            Player(*pd.data, self.height, self.width, map_arena)

        self.win.blit(map_arena.image, map_arena.rect)
        pygame.display.flip()

    def run(self) -> None:
        arena = Platform(self.win.get_height(), self.win.get_width())
        self.user.init(self.win.get_height() // 2 - arena.rect.size[1])

        while self.is_running:
            self.clock.tick(60)

            playerdata = self.network.send(self.user)
            
            self.user.move()

            self.refresh(arena, self.user, *playerdata)

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
