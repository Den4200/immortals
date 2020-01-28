from typing import List

import pygame

from .network import Network
from .player import Player


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

        pygame.display.set_caption('Immortals')

        self.network = Network(ip, port)
        self.user = self.network.connect()

    def refresh(self, *players: List['Player']) -> None:
        self.win.fill((255,255,255))

        for player in players:
            player.draw(self.win)

        pygame.display.update()

    def run(self) -> None:
        while self.is_running:
            self.clock.tick(60)
            players = self.network.send(self.user)

            self.user.move()
            self.refresh(self.user, *players)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
