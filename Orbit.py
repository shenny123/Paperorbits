import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP


pygame.init()
win = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

planets = []
bholes = []
planet_n = 0


class Planet(object):
    def __init__(self, x, y, radius, n):
        self.radius = radius
        self.x = x
        self.y = y
        self.velocity = (0, 0)
        self.n = n
        self.done = False
        self.last = (x, y)
        self.color = (255, 0, 0)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.mass = self.radius ** 3 * 1.0832 * 10 ** 8
        if not self.done:
            self.current_position = [mouse_x, mouse_y]
            self.velocity = [self.current_position[0] - self.last[0], self.current_position[1] - self.last[1]]
            self.last = [mouse_x, mouse_y]
        if self.done:
            for planet in planets:
                if planet.n != self.n and planet.done:
                    dx = planet.x - self.x
                    dy = planet.y - self.y
                    D = (dx ** 2 + dy ** 2) ** (0.5)
                    if D == 0: D = 0.000001
                    if D <= self.radius + planet.radius:
                        if self.radius > planet.radius:
                            self.radius = (self.radius ** 3 + planet.radius ** 3) ** (1 / 3)
                            self.velocity[0] = (self.mass * self.velocity[0] + planet.mass * planet.velocity[0]) / (
                                        self.mass + planet.mass)
                            self.velocity[1] = (self.mass * self.velocity[1] + planet.mass * planet.velocity[1]) / (
                                        self.mass + planet.mass)
                            planets.pop(planets.index(planet))
                        else:
                            planet.radius = (self.radius ** 3 + planet.radius ** 3) ** (1 / 3)
                            planet.velocity[0] = (self.mass * self.velocity[0] + planet.mass * planet.velocity[0]) / (
                                    self.mass + planet.mass)
                            planet.velocity[1] = (self.mass * self.velocity[1] + planet.mass * planet.velocity[1]) / (
                                    self.mass + planet.mass)
                            planets.pop(planets.index(self))
                    # print(D)
                    acc_g = ((6.67 * 10 ** (-11)) * planet.mass * gravityScale) / (D ** 2)

                    self.velocity[0] += (dx * acc_g) / D
                    self.velocity[1] += (dy * acc_g) / D
            for bhole in bholes:
                dx = bhole.x - self.x
                dy = bhole.y - self.y
                D = (dx ** 2 + dy ** 2)** (0.5)
                if D <= self.radius + bhole.radius:
                    planets.pop(planets.index(self))
                if D == 0: D = 0.000001
                acc_g = ((6.67 * 10 ** (-11)) * bhole.mass * gravityScale) / (D ** 2)

                self.velocity[0] += (dx * acc_g) / D
                self.velocity[1] += (dy * acc_g) / D

        if not down:
            self.done = True
        if not self.done:
            self.create()

    def create(self):
        if self.radius < 250:
            self.radius += 0.5
        self.x = mouse_x
        self.y = mouse_y

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), int(self.radius))


class black_hole(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 30
        self.velocity = (0, 0)
        self.last = (x, y)
        self.color = (255, 255, 255)
        self.mass = 1.0832 * 10 ** 14
        if down:
            self.create()

    def create(self):
        self.x = mouse_x
        self.y = mouse_y

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), int(self.radius))


class button():
    def __init__(self, color, x, y, width, height, text='', textSize = 60):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.textSize)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class textBox():
    def __init__(self, color, x, y, width, height, text='', textSize=60):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.textSize)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return False

class G():
    def __init__(self, color, x, y, width, height, textSize=60):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textSize = textSize
        self.text = 'G x     '

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont('comicsans', self.textSize)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return False

def redrawGameWindow():
    if not gameStart:
        win.fill("white")
        startButton.draw(win)
        gameName.draw(win)
        creditsFrame.draw(win)
    else:
        win.fill("black")

        for planet in planets:
            planet.draw(win)
        for bhole in bholes:
            bhole.draw(win)
        exitButton.draw(win)
        gravityFrame.draw(win)
        gravityUp.draw(win)
        gravityDown.draw(win)
        text = font.render(str(gravityScale),1, (0,0,0))
        win.blit(text, (680, 180))
        planetButton.draw(win)
        if blackHole == 1:
            text1 = font1.render('Planets', 1, (0,0,0))
        elif blackHole == -1:
            text1 = font1.render('Blackholes', 1, (0,0,0))
        win.blit(text1, (1335, 174))
        clearAll.draw(win)
        if prompt:
            promptFrame.draw(win)
            yesPrompt.draw(win)
            noPrompt.draw(win)

    pygame.display.update()


radiusLoop = 0
down = False
run = True
gameStart = False
startButton = button((33, 64, 166), 400, 500, 250, 100, 'Start')
gameName = textBox((255,255,255), 400, 250, 300, 150, 'Paper Orbits', 80)
exitButton = button((33, 64, 166), 300, 150, 200, 70, 'Quit')
prompt = False
promptFrame = textBox((255,255,255),800,500,300,125,'Are you sure?', 50)
yesPrompt = button((125, 125, 125), 820, 580, 50, 30, 'Yes', 40)
noPrompt = button((125, 125, 125), 1000, 580, 50, 30, 'No', 40)
paused = False
gravityScale = 1.0
gravityFrame = G((33,64,166), 600, 150, 150, 100)
gravityUp = button((33,64,166), 760, 150, 50, 100, '+')
gravityDown = button((33,64,166), 540, 150, 50, 100, '-')
font = pygame.font.SysFont('comicsans', 60, True)
font1 = pygame.font.SysFont('comicsans', 30, True)
blackHole = 1
freeze = False
planetButton = button((255, 255, 255), 1200, 150, 300, 70, 'Creating                       ', 30)
clearAll = button((255,255,255), 1460, 800, 80, 80, "Clear", 30)
creditsFrame = textBox((255,255,255), 430, 650, 100, 50, 'by Shen Zhang', 30)
while run:
    clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if gameStart:
            if not paused:
                if gravityUp.isOver(pos) or gravityDown.isOver(pos): freeze = True
                else: freeze = False
                if event.type == MOUSEBUTTONDOWN and blackHole == 1 and not freeze:
                    planets.append(Planet(mouse_x, mouse_y, 0.00001, planet_n))
                    planet_n += 1
                    down = True
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    down = False
                if event.type == MOUSEBUTTONDOWN and blackHole == -1 and not freeze:
                    bholes.append(black_hole(mouse_x, mouse_y))
                    down = True
                if event.type == MOUSEBUTTONUP and event.button == 3:
                    down = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exitButton.isOver(pos):
                        prompt = True
                        paused = True
                    if gravityUp.isOver(pos):
                        if 5 >= gravityScale >= 0:
                            gravityScale += 0.1
                            gravityScale = round(gravityScale * 10) / 10
                            if gravityScale == 5.1: gravityScale = 5
                            print("pressed")
                            print(gravityScale)
                    if gravityDown.isOver(pos):
                        if 5 >= gravityScale >= 0:
                            gravityScale -= 0.1
                            gravityScale = round(gravityScale * 10) / 10
                            print(gravityScale)
                            if gravityScale == -0.1: gravityScale = 0
                    if planetButton.isOver(pos):
                        blackHole *= -1
                    if clearAll.isOver(pos):
                        planets.clear()
                        bholes.clear()


            if paused:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yesPrompt.isOver(pos):
                        run = False
                    elif noPrompt.isOver(pos):
                        prompt = False
                        paused = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.isOver(pos):
                    gameStart = True

    if keys[pygame.K_DELETE]:
        planets.clear()
        bholes.clear()
    if not paused:
        for planet in planets:
            planet.update()
    redrawGameWindow()

pygame.quit()
