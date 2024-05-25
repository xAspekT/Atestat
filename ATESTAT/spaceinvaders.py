import pygame
import random

pygame.init()

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SHIP_WIDTH = 120
SHIP_HEIGHT = 120
SHIP_SPEED = 5.5

BULLET_WIDTH = 25
BULLET_HEIGHT = 10
BULLET_SPEED = 7
BULLET_COOLDOWN = 250

ENEMY_WIDTH = 70
ENEMY_HEIGHT = 70
ENEMY_SPEED = 3

FPS = 60
ENEMY_SPAWN_RATE = 60  # Higher means fewer enemies

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Game")

ship_image = pygame.image.load('ship.png')
ship_image = pygame.transform.scale(ship_image, (SHIP_WIDTH, SHIP_HEIGHT))

enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (BULLET_WIDTH, BULLET_HEIGHT))

background_image = pygame.image.load('background.jpeg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

shoot_sound = pygame.mixer.Sound('shoot_sound.mp3')
enemy_death_sound = pygame.mixer.Sound('enemy_death_sound.mp3')

shoot_sound.set_volume(0.2)
enemy_death_sound.set_volume(0.3)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT))
        self.image.fill(GREEN)
        self.image = ship_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed = SHIP_SPEED
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > BULLET_COOLDOWN:
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(RED)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(BLACK)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

ship = Ship()
all_sprites.add(ship)

running = True
clock = pygame.time.Clock()
score = 0
level_end_x = SCREEN_WIDTH - 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if hits:
        score += len(hits)
        enemy_death_sound.play()

    if ship.rect.right >= level_end_x:
        print("You win! Final score:", score)
        running = False

    if random.randint(1, ENEMY_SPAWN_RATE) == 1:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    screen.blit(background_image, (0, 0))

    all_sprites.draw(screen)

    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
