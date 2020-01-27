import pygame
from network import Network
from player import Player

width = 1920
height = 1080
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, *players):
    win.fill((255,255,255))

    for player in players:
        player.draw(win)

    pygame.display.update()


def main():
    run = True
    network = Network()
    user = network.user
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        players = network.send(user)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        user.move()
        redrawWindow(win, user, *players)

main()
