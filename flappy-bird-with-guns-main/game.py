import pygame
from pipe import Pipe


class Game:
    W_WIDTH = 1400
    W_HEIGHT = 1050
    W_BG = pygame.image.load("assets/background.jpg")
    CLOCK = pygame.time.Clock()
    FPS = 30
    PLAY_BTN_SPRITE = pygame.transform.scale(
        pygame.image.load("assets/play.png"),
        (480, 480)
    )
    PIPE_SPRITE = pygame.image.load("assets/pipe.png")
    SECONDS_BETWEEN_PIPES = 3
    frames_since_last_pipe = 0
    pipes = []
    game_started = False

    def __init__(self, player):
        self.window = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))
        self.window.blit(self.W_BG, (0, 0))
        self.setUpMenu()
        self.player = player

    def update(self):
        self.CLOCK.tick(self.FPS)
        events = pygame.event.get()
        self.window.blit(self.W_BG, (0, 0))
        

        for event in events:
            if event.type == pygame.QUIT:
                quit()

        if not self.game_started:
            self.drawMenu()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    print(x, y)
                    if self.clickOnPlay(x, y):
                        self.startGame()
            return

        # After game strted
        self.player.update(self.window)
        for pipe in self.pipes:
            pipe.update(self.window)

        # Events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stopGame()
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.jump()

        # Keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.moveLeft()
        if keys[pygame.K_d]:
            self.player.moveRight()

        # Collisions
        if self.player.touchesPipes(self.pipes):
            self.reset()

        # Creating pipes
        self.frames_since_last_pipe += 1
        if self.frames_since_last_pipe > self.FPS * self.SECONDS_BETWEEN_PIPES:
            self.createPipe()
            self.frames_since_last_pipe = 0

        # Deleting pipes
        for pipe in self.pipes:
            if pipe.x < -300:
                self.pipes.remove(pipe)

    def setUpMenu(self):
        pass

    def drawMenu(self):
        self.window.blit(self.PLAY_BTN_SPRITE,
                         (self.W_WIDTH / 2 - 350/2, self.W_HEIGHT / 2 - 150/2))

    def startGame(self):
        self.game_started = True

    def stopGame(self):
        self.game_started = False

    def createPipe(self):
        pipe = Pipe(self.PIPE_SPRITE, self.W_WIDTH)
        self.pipes.append(pipe)

    def reset(self):
        self.pipes = []
        self.player.reset()

    def clickOnPlay(self, mouseX, mouseY):
        minx = self.W_WIDTH / 2 - 350/2
        maxx = self.W_WIDTH / 2 - 350/2 + 350

        miny = self.W_HEIGHT / 2 - 150/2
        maxy = self.W_HEIGHT / 2 - 150/2 + 150
        return mouseX > minx and mouseX < maxx and mouseY > miny and mouseY < maxy
