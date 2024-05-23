import pygame
from game import Game
from player import Player

pygame.init()

player = Player()
game = Game(player)

while True:
    game.update()

    pygame.display.update()