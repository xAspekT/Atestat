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
SHIP_SPEED = 6


BULLET_WIDTH = 25
BULLET_HEIGHT = 10
BULLET_SPEED = 7

ENEMY_WIDTH = 70
ENEMY_HEIGHT = 70
ENEMY_SPEED = 3

FPS = 60
ENEMY_SPAWN_RATE = 60  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Conquerors")

ship_image = pygame.image.load('ship.png')
ship_image = pygame.transform.scale(ship_image, (SHIP_WIDTH, SHIP_HEIGHT))

enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (BULLET_WIDTH, BULLET_HEIGHT))

background_image = pygame.image.load('background.jpeg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT))
        self.image.fill(GREEN)
        self.image = ship_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed = SHIP_SPEED
        self.health = 3  

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

def draw_button(screen, rect, text, font, color):
    pygame.draw.rect(screen, WHITE, rect)
    draw_text(screen, text, font, color, rect)
            
def draw_text(screen, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect.topleft)

def show_pause_menu():
    resume_button_image = pygame.image.load('resume_button.png')
    resume_button_image = pygame.transform.scale(resume_button_image, (300, 70))

    high_scores_button_image = pygame.image.load('high_scores_button.png')
    high_scores_button_image = pygame.transform.scale(high_scores_button_image, (300, 70))

    quit_button_image = pygame.image.load('quit_button.png')
    quit_button_image = pygame.transform.scale(quit_button_image, (300, 70))

    button_width = resume_button_image.get_width()
    button_height = resume_button_image.get_height()
    button_x = (SCREEN_WIDTH - button_width) // 2
    resume_button_y = (SCREEN_HEIGHT - 3 * button_height) // 2
    high_scores_button_y = resume_button_y + button_height + 20
    quit_button_y = high_scores_button_y + button_height + 20

    screen.blit(resume_button_image, (button_x, resume_button_y))
    screen.blit(high_scores_button_image, (button_x, high_scores_button_y))
    screen.blit(quit_button_image, (button_x, quit_button_y))

    pygame.display.flip()

    return resume_button_image.get_rect(topleft=(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100)), \
           high_scores_button_image.get_rect(topleft=(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2)), \
           quit_button_image.get_rect(topleft=(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 100))

def show_quit_confirmation():
    font = pygame.font.Font(None, 74)
    draw_text(screen, "Really Quit?", font, WHITE, pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 200, 200, 50))

    yes_button_image = pygame.image.load('yes_button.png')
    yes_button_image = pygame.transform.scale(yes_button_image, (200, 70))
    no_button_image = pygame.image.load('no_button.png')
    no_button_image = pygame.transform.scale(no_button_image, (200, 70))

    button_x = (SCREEN_WIDTH - 200) // 2
    button_height = yes_button_image.get_height()

    total_buttons_height = button_height * 2 + 20
    button_y = (SCREEN_HEIGHT - total_buttons_height) // 2

    yes_button_y = button_y
    no_button_y = button_y + button_height + 20

    screen.blit(yes_button_image, (button_x, yes_button_y))
    screen.blit(no_button_image, (button_x, no_button_y))

    pygame.display.flip()
    return pygame.Rect(button_x, yes_button_y, 200, 70), pygame.Rect(button_x, no_button_y, 200, 70)


def show_high_scores():
    font = pygame.font.Font(None, 36)
    scores_rect = pygame.Rect(SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2 - 200, 250, 400)
    draw_text(screen, "High Scores:", font, WHITE, scores_rect.move(0, -50))

    draw_text(screen, "1. Player1 - 1000", font, WHITE, scores_rect.move(0, 0))
    draw_text(screen, "2. Player2 - 800", font, WHITE, scores_rect.move(0, 50))
    draw_text(screen, "3. Player3 - 600", font, WHITE, scores_rect.move(0, 100))
    draw_text(screen, "Press Esc to return", font, WHITE, scores_rect.move(0, 200))

    pygame.display.flip()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

ship = Ship()
all_sprites = pygame.sprite.Group()
all_sprites.add(ship)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

running = True
paused = False
showing_high_scores = False
showing_quit_confirmation = False
clock = pygame.time.Clock()
score = 0
level_end_x = SCREEN_WIDTH - 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                if showing_quit_confirmation:
                    showing_quit_confirmation = False
                    paused = True
                elif showing_high_scores:
                    showing_high_scores = False
                    paused = True
                elif not paused:
                    paused = True
                else:
                    paused = False
            elif event.key == pygame.K_SPACE and not paused and not showing_high_scores and not showing_quit_confirmation:
                ship.shoot()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if paused and not showing_high_scores and not showing_quit_confirmation:
                if resume_button_rect.collidepoint(mouse_pos):
                    paused = False
                elif high_scores_button_rect.collidepoint(mouse_pos):
                    showing_high_scores = True
                    paused = False
                elif quit_button_rect.collidepoint(mouse_pos):
                    showing_quit_confirmation = True
                    paused = False
            elif showing_quit_confirmation:
                yes_button_rect, no_button_rect = show_quit_confirmation()
                if yes_button_rect.collidepoint(mouse_pos):
                    running = False
                elif no_button_rect.collidepoint(mouse_pos):
                    showing_quit_confirmation = False
                    paused = True

    if not paused and not showing_high_scores and not showing_quit_confirmation:
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
            
    elif paused:
        screen.blit(background_image, (0, 0))
        resume_button_rect, high_scores_button_rect, quit_button_rect = show_pause_menu()
            
    elif showing_high_scores:
        screen.blit(background_image, (0, 0))
        show_high_scores()
            
    elif showing_quit_confirmation:
        screen.blit(background_image, (0, 0))
        yes_button_rect, no_button_rect = show_quit_confirmation()
            

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

