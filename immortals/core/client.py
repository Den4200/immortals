from typing import Dict, Tuple

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

        self._playerdata = self.network.recieve()
        self._player: Player = None
        self.active_sprites = dict()

    @property
    def player(self):
        return self._player

    @property
    def playerdata(self):
        return self._playerdata

    def update_active_sprites(self):
        for sprite in self.active_sprites.values():
            sprite.update()

    def draw_active_sprites(self):
        for sprite in self.active_sprites.values():
            self.win.blit(sprite.image, sprite.rect)

    def refresh(self, map_arena, playerdata: Dict[Tuple[str, int], 'PlayerData']) -> None:

        if len(playerdata) > self.player_count:

            for addr in playerdata:
                if addr not in self.active_sprites:
                    self.active_sprites.update({
                        addr: Player(
                            *playerdata[addr].data,
                            self.height, self.width,
                            map_arena
                        )
                    })
                    self.player_count += 1

        active_lst = list(self.active_sprites)[1:]
        for addr in active_lst:
            try:
                self.active_sprites[addr].set_data(playerdata[addr].data)

            except KeyError:
                self.active_sprites.pop(addr)
                self.player_count -= 1

        if self._player.rect.right > self.width:
            self._player.rect.right = self.width

        if self._player.rect.left < 0:
            self._player.rect.left = 0

        self.update_active_sprites()
        map_arena.update()
        pygame.display.flip()

    def run(self) -> None:
        map_ = Haven(self.win)
        self._player = Player(*self._playerdata[1].data, self.height, self.width, map_)
        self.active_sprites.update({
            self._playerdata[0]: self._player
        })

        while self.is_running:
            self.clock.tick(60)

            self._playerdata[1].data = self._player.data

            self.network.send(self._playerdata)
            playerdata = self.network.recieve()

            self.refresh(map_, playerdata)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a:
                        self._player.move_left()

                    if event.key == pygame.K_d:
                        self._player.move_right()

                    if event.key == pygame.K_SPACE:
                        self._player.jump()

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a and self._player.x_delta < 0:
                        self._player.stop()

                    if event.key == pygame.K_d and self._player.x_delta > 0:
                        self._player.stop()

            map_.draw()
            self.draw_active_sprites()

# http://programarcadegames.com/python_examples/show_file.php?file=platform_jumper.py
