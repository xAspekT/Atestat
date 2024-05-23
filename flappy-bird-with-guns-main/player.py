import pygame


def collide(image1, x1, y1, image2, x2, y2):
    x = x2 - x1
    y = y2 - y1
    mask1 = pygame.mask.from_surface(image1)
    mask2 = pygame.mask.from_surface(image2)
    return mask1.overlap(mask2, (x, y)) != None


class Player:
    Y_ACCELERATION = 13
    X_ACCELERATION = 10
    y = 100
    vy = 0
    x = 100
    vx = 0
    sprite = pygame.image.load("assets/jetpackguy.png")

    def __init__(self):
        self.sprite = pygame.transform.scale(self.sprite, (150, 150))

    def moveLeft(self):
        self.vx = -1 * self.X_ACCELERATION

    def moveRight(self):
        self.vx = self.X_ACCELERATION

    def jump(self):
        self.vy = -1 * self.Y_ACCELERATION

    def update(self, window):
        # Move vertically
        if self.y + self.vy > 0 and self.y + self.vy < window.get_height():
            self.y = self.y + self.vy
        self.vy = self.vy + 1

        # Move horizontally
        self.x = self.x + self.vx
        if self.vx < 0:
            self.vx = self.vx + 1
        if self.vx > 0:
            self.vx = self.vx - 1

        pygame.transform.rotate(self.sprite, self.vy)

        # Draw player
        window.blit(self.sprite, (self.x, self.y))

    def touchesPipes(self, pipes):
        for pipe in pipes:
            if collide(self.sprite, self.x, self.y, pipe.sprite, pipe.x, pipe.y):
                return True

        return False

    def reset(self):
        self.x = 100
        self.y = 100
        self.vx = 0
        self.vy = 0
