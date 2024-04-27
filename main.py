from random import randint
import pygame
import math
pygame.init()


class simState():
    def __init__(self):
        self.windowX = 1000
        self.windowY = 700
        self.theWindowThing = pygame.display.set_mode([self.windowX, self.windowY])
        self.shouldRun = True
        self.q = None
        self.planets = []
        self.simElements = []
        self.colorTrail = 3  # 0 = none, 1 = solid, 2 = multicolor, 3 = multi-brightness, 4 - fading (doesn't work)
        self.grayFix = 3  # only applies when colorTrail is set to 3
        # 0 = none (all planets eventually turn gray)
        # 1 = do not change to gray (doesn't work well)
        # 2 = revert to initial colors when turns gray
        # 3 = revert to a while ago if near gray (works best)
        self.colorDistanceMin = 20
        # Higher values mean less gray, but too high means too many resets (if all 3 colors are whithin this distance)
        self.colorDistanceMinLow = 15
        # Higher values mean less gray, but too high means too many resets (if any 2 colors are whithin this distance)
        self.colorRecordTime = 750
        # Higher values mean reverting is more noticeable, but fixes gray better
        self.numberThing = 1
        self.hue = None
        self.funny = None


class quitDetector():
    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("bye")
                sm.shouldRun = False
                pygame.quit()
                quit()


sm = simState()
sm.q = quitDetector()
sm.simElements = []


class planet():
    def setColor(self):
        # self.colorValue = self.mass2 * 5 + self.mass2 * 20
        if sm.hue is None:
            self.r = randint(51, 255)
            self.g = randint(50, 252)
            self.b = randint(51, 255)
            self.color = (self.r, self.g, self.b)
            self.initR = self.r
            self.initG = self.g
            self.initB = self.b
            self.color2reset = 0
            self.color3reset = 0
            self.prevR2 = self.r
            self.prevG2 = self.g
            self.prevB2 = self.b
        else:
            self.r = sm.hue
            self.g = 50
            self.b = 100
            self.color = (self.r, self.g, self.b)
            self.initR = self.r
            self.initG = self.g
            self.initB = self.b
            self.color2reset = 0
            self.prevR2 = self.r
            self.prevG2 = self.g
            self.prevB2 = self.b

    def setColor2(self):
        self.color3reset += 1
        self.color2reset += 1
        if self.color2reset > sm.colorRecordTime:
            self.prevR2 = self.r
            self.prevG2 = self.g
            self.prevB2 = self.b
        if sm.colorTrail == 2:
            self.r += randint(-5, 5)
            if self.r > 255:
                self.r = 255
            if self.r < 10:
                self.r = 10
            self.g += randint(-5, 5)
            if self.g > 254:
                self.g = 254
            if self.g < 9:
                self.g = 9
            self.b += randint(-5, 5)
            if self.b > 255:
                self.b = 255
            if self.b < 10:
                self.b = 10
            self.color = (self.r, self.g, self.b)
        if sm.colorTrail == 3:
            self.prevR = self.r
            self.prevG = self.g
            self.prevB = self.b
            self.randomThing = randint(-5, 5)
            self.r += self.randomThing
            if self.r > 250:
                self.r = 250
            if self.r < 10:
                self.r = 10
            self.g += self.randomThing
            if self.g > 249:
                self.g = 249
            if self.g < 9:
                self.g = 9
            self.b += self.randomThing
            if self.b > 250:
                self.b = 250
            if self.b < 10:
                self.b = 10
            self.revert = False
            if sm.grayFix == 3:
                if abs(self.r - self.b) <= sm.colorDistanceMinLow:
                    self.revert = True
                if abs(self.b - self.g) <= sm.colorDistanceMinLow:
                    self.revert = True
                if abs(self.g - self.r) <= sm.colorDistanceMinLow:
                    self.revert = True
                if abs(self.r - self.b) <= sm.colorDistanceMin and abs(self.b - self.g) <= sm.colorDistanceMin and abs(self.g - self.r) <= sm.colorDistanceMin:
                    self.revert = True
            else:
                if self.r == self.b:
                    self.revert = True
                if self.b == self.g:
                    self.revert = True
                if self.g == self.r:
                    self.revert = True
            if self.revert:
                if sm.grayFix == 3:
                    self.r = self.prevR2
                    self.b = self.prevB2
                    self.g = self.prevG2
                if sm.grayFix == 2:
                    self.r = self.initR
                    self.b = self.initB
                    self.g = self.initG
                elif sm.grayFix == 1:
                    self.r = self.prevR
                    self.g = self.prevG
                    self.b = self.prevB
            else:
                self.color = (self.r, self.g, self.b)
        if self.revert and self.color3reset < 3:
            self.setColor()

    def __init__(self, mass, x, y, xv, yv, thenumberThing):
        self.simScale = 8
        self.timeScale = 1  # Doesn't work
        if mass is None:
            self.mass = randint(2 * 13, 15 * 13)
        else:
            self.mass = mass * 15.5
        # self.x = randint(50, 950 * self.simScale)
        # self.y = randint(50, 650 * self.simScale)
        if x is None or y is None:
            print("Planet #" + str(thenumberThing) + " (Color " + str(sm.hue) + "):")
        if x is None:
            self.x = randint(0, sm.windowX * self.simScale)
            print("Random starting x: " + str(self.x))
        else:
            self.x = x * self.simScale
        if y is None:
            self.y = randint(0, sm.windowY * self.simScale)
            print("Random starting y: " + str(self.y))
        else:
            self.y = y * self.simScale
        # self.xSpeed = 10.5 - mass  # What is this?
        if xv is None:
            self.xvel = randint(-5, 5)
        else:
            self.xvel = xv
        if yv is None:
            self.yvel = randint(-5, 5)
        else:
            self.yvel = yv
        self.setColor()
        self.xa = 0
        self.ya = 0

    def update1(self, sm):
        if False:
            if self.y > sm.windowY:
                sm.simElements.remove(self)
                sm.planets.remove(self)
            if self.x > sm.windowX:
                sm.simElements.remove(self)
                sm.planets.remove(self)
            if self.y < 0:
                sm.simElements.remove(self)
                sm.planets.remove(self)
            if self.x < 0:
                sm.simElements.remove(self)
                sm.planets.remove(self)

        # math stuff
        if sm.funny == 1:
            for thePlanet in sm.planets:
                r = math.sqrt((self.y - thePlanet.y)**2 +
                            (self.x - thePlanet.x)**2)
                if (r > 0):
                    gravitationalConstant = 50
                    a = gravitationalConstant * thePlanet.mass / (r ** 2)
                    theta = math.atan2((self.y - thePlanet.y),
                                    (self.x - thePlanet.x))
                    self.xa = a * math.cos(theta)
                    self.ya = a * math.sin(theta)
                    self.xvel += self.xa
                    self.yvel -= self.ya
            # if self.isOffscreen:
            self.setColor2()
        else:
            for thePlanet in sm.planets:
                r = math.sqrt((self.y - thePlanet.y)**2 +
                            (self.x - thePlanet.x)**2)
                if (r > 0):
                    gravitationalConstant = 50
                    a = gravitationalConstant * thePlanet.mass / (r ** 2)
                    theta = math.atan2((self.y - thePlanet.y),
                                    (self.x - thePlanet.x))
                    self.xa = a * math.cos(theta)
                    self.ya = a * math.sin(theta)
                    self.xvel += self.xa / self.timeScale
                    self.yvel -= self.ya / self.timeScale
            # if self.isOffscreen:
            self.setColor2()

    def update2(self, sm):
        if sm.funny == 1:
            self.x -= self.xvel ** (6 * self.timeScale)
            self.y += self.yvel ** (6 * self.timeScale)
        elif sm.funny == 2:
            self.x += self.yvel
            self.y -= self.xvel
        else:
            self.x -= self.xvel * self.timeScale
            self.y += self.yvel * self.timeScale

    def draw(self, sm):
        if False:
            pygame.draw.circle(sm.theWindowThing, (self.color), (self.x / self.simScale,
                               self.y / self.simScale), self.mass / self.simScale)
        else:
            self.isOffscreen = False
            self.offscreenOffset = 5
            if self.y > (sm.windowY / self.simScale) + self.offscreenOffset:
                self.isOffscreen = True
            if self.x > (sm.windowX / self.simScale) + self.offscreenOffset:
                self.isOffscreen = True
            if self.y < 0 - self.offscreenOffset:
                self.isOffscreen = True
            if self.x < 0 - self.offscreenOffset:
                self.isOffscreen = True
            if self.isOffscreen:
                pygame.draw.circle(sm.theWindowThing, (self.color), (self.x / self.simScale,
                    self.y / self.simScale), self.mass / self.simScale)
            else:
                print("Not being drawn")


def spawn(sm, m, x, y, xv, yv):
    # newMass = randint(1, 10)
    newPlanet = planet(m, x, y, xv, yv, sm.numberThing)
    sm.numberThing += 1
    sm.planets.append(newPlanet)
    sm.simElements.append(newPlanet)
    if sm.hue is not None:
        sm.hue += 100
        if sm.hue > 254:
            sm.hue = 0


if False:
    spawn(sm, None, None, None, None, None)
    spawn(sm, None, None, None, None, None)
elif False:
    spawn(sm, 10, 600, 200, None, 0)
    spawn(sm, 10, 650, 250, -1, None)
else:
    spawn(sm, 3.051, 570, 200, 0.4, 0)
    spawn(sm, 6.371, 650, 260, -0.4, 0)

if sm.funny != None:
    print("funny mode activated")
    sm.theWindowThing.fill((0, 10, 0))
else:
    sm.theWindowThing.fill((6, 0, 20))  # Old: 14, 10, 35
while sm.shouldRun:
    if sm.colorTrail == 0:
        sm.theWindowThing.fill((14, 10, 35))
    if sm.colorTrail == 4:
        sm.theWindowThing.set_alpha(100)  # 0 is fully transparent and 255 fully opaque.
        sm.theWindowThing.fill((14, 10, 35, 50))
    for ge in sm.simElements:
        ge.update1(sm)
    for ge in sm.simElements:
        ge.update2(sm)
        ge.draw(sm)
    sm.q.update(sm)
    pygame.display.flip()
