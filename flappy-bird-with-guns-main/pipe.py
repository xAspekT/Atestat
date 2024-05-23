import random
import pygame


class Pipe:
    MIN_PIPE_Y = -900
    MAX_PIPE_Y = -150
    GAP_Y_OFFSET = 1100
    GAP_X_SIZE = 200
    GAP_Y_SIZE = 120
    X_ACCELERATION = -8

    def __init__(self, sprite, x):
        self.sprite = pygame.transform.scale(sprite, (120, 2100))
        self.y = random.randrange(self.MIN_PIPE_Y, self.MAX_PIPE_Y, 50)
        self.x = x

    def update(self, window):
        self.x = self.x + self.X_ACCELERATION
        window.blit(self.sprite, (self.x, self.y))
