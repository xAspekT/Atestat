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
BULLET_COOLDOWN = 169

ENEMY_WIDTH = 70
ENEMY_HEIGHT = 70
ENEMY_SPEED = 3

BIGENEMY_WIDTH = int(ENEMY_WIDTH * 1.5)
BIGENEMY_HEIGHT = int(ENEMY_HEIGHT * 1.5)
BIGENEMY_SPEED = 2

GIANTENEMY_WIDTH = int(ENEMY_WIDTH * 3)
GIANTENEMY_HEIGHT = int(ENEMY_HEIGHT * 3)
GIANTENEMY_SPEED = ENEMY_SPEED * 0.5

FPS = 60

ENEMY_SPAWN_RATE = 100  #cu cat e val mai mare cu atat sunt mai putini inamici

restart_button_image = pygame.image.load('restart_button.png')
restart_button_image = pygame.transform.scale(restart_button_image, (200, 70))
restart_button_rect = restart_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

quit_button_image = pygame.image.load('quit_button.png')
quit_button_image = pygame.transform.scale(quit_button_image, (200, 70))
quit_button_rect = quit_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Conquerors")

ship_image = pygame.image.load('ship.png')
ship_image = pygame.transform.scale(ship_image, (SHIP_WIDTH, SHIP_HEIGHT))

enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

bigenemy_image = pygame.image.load('bigenemy.png')
bigenemy_image = pygame.transform.scale(bigenemy_image, (BIGENEMY_WIDTH, BIGENEMY_HEIGHT))

giantenemy_image = pygame.image.load('giant.png')
giantenemy_image = pygame.transform.scale(giantenemy_image, (GIANTENEMY_WIDTH, GIANTENEMY_HEIGHT))

bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (BULLET_WIDTH, BULLET_HEIGHT))

background_image = pygame.image.load('background.jpeg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

shoot_sound = pygame.mixer.Sound('shoot_sound.mp3')
shoot_sound.set_volume(0.05)
enemy_death_sound = pygame.mixer.Sound('enemy_death_sound.mp3')
enemy_death_sound.set_volume(0.8)
giant_enemy_death_sound = pygame.mixer.Sound('giant_enemy_death_sound.mp3')
giant_enemy_death_sound.set_volume(1.2)
big_enemy_death_sound = pygame.mixer.Sound('big_enemy_death_sound.mp3')
big_enemy_death_sound.set_volume(0.7)
pygame.mixer.music.load('ost.mp3')
pygame.mixer.music.set_volume(1.1)
pygame.mixer.music.play(-1)
pause_sound = pygame.mixer.Sound('pause.mp3')

def play_pause_sound(volume):
    pause_sound.set_volume(volume)
    if pygame.mixer.get_busy():
        pygame.mixer.stop()
    pause_sound.play()

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

def show_game_over_screen(score):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("You Died", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    
    pygame.display.flip()
    
    restart_button_rect = restart_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(restart_button_image, restart_button_rect)

    screen.blit(quit_button_image, quit_button_rect)

    pygame.display.flip()

    return restart_button_rect, quit_button_rect

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

    quit_button_image = pygame.image.load('quit_button.png')
    quit_button_image = pygame.transform.scale(quit_button_image, (200, 70))

    button_width = resume_button_image.get_width()
    button_height = resume_button_image.get_height()
    button_x = (SCREEN_WIDTH - button_width) // 2
    resume_button_y = (SCREEN_HEIGHT - 2 * button_height) // 2
    quit_button_y = resume_button_y + button_height + 20

    screen.blit(resume_button_image, (button_x, resume_button_y))
    quit_button_x = (SCREEN_WIDTH - quit_button_image.get_width()) // 2
    
    screen.blit(quit_button_image, (quit_button_x, quit_button_y))

    pygame.display.flip()

    return resume_button_image.get_rect(topleft=(button_x, resume_button_y)), \
           quit_button_image.get_rect(topleft=(quit_button_x, quit_button_y))


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


all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BIGENEMY_WIDTH, BIGENEMY_HEIGHT))
        self.image.fill(BLACK)
        self.image = bigenemy_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - BIGENEMY_HEIGHT)
        self.speed = BIGENEMY_SPEED
        self.health = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class GiantEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GIANTENEMY_WIDTH, GIANTENEMY_HEIGHT))
        self.image.fill(BLACK)
        self.image = giantenemy_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - GIANTENEMY_HEIGHT)
        self.speed = GIANTENEMY_SPEED
        self.health = 20

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


ship = Ship()
all_sprites = pygame.sprite.Group()
all_sprites.add(ship)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bigenemies = pygame.sprite.Group()
giantenemies = pygame.sprite.Group()

running = True
paused = False
showing_quit_confirmation = False
clock = pygame.time.Clock()
score = 0
last_giant_spawn_score = 0
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
                    pygame.mixer.music.pause()
                    play_pause_sound(0.5)
                elif not paused:
                    paused = True
                    pygame.mixer.music.pause()
                    play_pause_sound(0.5)
                else:
                    paused = False
                    play_pause_sound(0)
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_SPACE and not paused and not showing_quit_confirmation:
                ship.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if paused and not showing_quit_confirmation:
                if resume_button_rect.collidepoint(mouse_pos):
                    paused = False
                    pygame.mixer.music.unpause()
                    play_pause_sound(0)
                elif quit_button_rect.collidepoint(mouse_pos):
                    showing_quit_confirmation = True
                    paused = False
                    pygame.mixer.music.pause()
                    play_pause_sound(0.5)
            elif showing_quit_confirmation:
                yes_button_rect, no_button_rect = show_quit_confirmation()
                if yes_button_rect.collidepoint(mouse_pos):
                    running = False
                elif no_button_rect.collidepoint(mouse_pos):
                    showing_quit_confirmation = False
                    paused = True

    if not paused and not showing_quit_confirmation:
            all_sprites.update()
            
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            if hits:
                score += len(hits)
                enemy_death_sound.play()
            
            if random.randint(1, ENEMY_SPAWN_RATE) == 1:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            
            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(text, (10, 10))

            health_text = font.render(f'Health: {ship.health}', True, WHITE)
            screen.blit(health_text, (SCREEN_WIDTH - 150, 10))
            all_sprites.draw(screen)
            
    elif paused:
        screen.blit(background_image, (0, 0))
        resume_button_rect, quit_button_rect = show_pause_menu()
            
    elif showing_quit_confirmation:
        screen.blit(background_image, (0, 0))
        yes_button_rect, no_button_rect = show_quit_confirmation()
            
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if hits:
        score += len(hits)

    big_hits = pygame.sprite.groupcollide(bullets, bigenemies, True, False)
    for big_enemy_list in big_hits.values():
        for big_enemy in big_enemy_list:
            big_enemy.health -= 1
            if big_enemy.health <= 0:
                big_enemy.kill()
                big_enemy_death_sound.play()
                score += 3

    giant_hits = pygame.sprite.groupcollide(bullets, giantenemies, True, False)
    for giant_enemy_list in giant_hits.values():
        for giant_enemy in giant_enemy_list:
            giant_enemy.health -= 1
            if giant_enemy.health <= 0:
                giant_enemy.kill()
                giant_enemy_death_sound.play()
                score += 15

    collisions = pygame.sprite.spritecollide(ship, enemies, True)
    if collisions:
        ship.health -= 1

    big_collisions = pygame.sprite.spritecollide(ship, bigenemies, True)
    if big_collisions:
        ship.health -= 1

    giant_collisions = pygame.sprite.spritecollide(ship, giantenemies, True)
    if giant_collisions:
        ship.health -= 3

    if random.randint(1, ENEMY_SPAWN_RATE) == 1:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    if score >= 10 and random.randint(1, ENEMY_SPAWN_RATE * 2) == 1:
        bigenemy = BigEnemy()
        all_sprites.add(bigenemy)
        bigenemies.add(bigenemy)

    if score >= 50 and score % 25 == 0 and score != last_giant_spawn_score:
        giantenemy = GiantEnemy()
        all_sprites.add(giantenemy)
        giantenemies.add(giantenemy)
        last_giant_spawn_score = score
    
    if ship.health <= 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('joever.mp3')
        pygame.mixer.music.play()
        show_game_over_screen(score)
        waiting_for_action = True
        while waiting_for_action:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button_rect.collidepoint(mouse_pos):
                        ship.health = 3
                        score = 0

                        ship.rect.center = (100, SCREEN_HEIGHT // 2)

                        all_sprites.empty()
                        bullets.empty()
                        enemies.empty()
                        bigenemies.empty()
                        giantenemies.empty()

                        all_sprites.add(ship)

                        running = True
                        waiting_for_action = False
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
