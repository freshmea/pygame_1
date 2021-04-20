import pygame, sys, random
from pygame.locals import *
pygame.init()
pygame.display.set_caption("움직이는 원")
screen = pygame.display.set_mode((640, 480))
xpos= 50
ypos= 200
clock = pygame.time.Clock()
raindrop_spawn_time=0
rain_quantity=11

mike_umbrella_image = pygame.image.load("images/Mike_umbrella.png").convert()
cloud_image = pygame.image.load(("images/cloud.png")).convert()

"""구름 클래스 정의"""
class Cloud:
    def __init__(self):
        self.x = 300
        self.y = 50
    def move(self):
        if self.x >= 640:
            self.x = 1
        self.x += 1
    def rain(self):
        raindrops.append(Raindrop(random.randint(self.x, self.x+300), self.y+100))
    def draw(self):
        screen.blit(cloud_image,(self.x, self.y))

"""마이크 클래스 정의"""
class Mike:
    def __init__(self):
        self.x = 300
        self.y = 200

    def keydown(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RIGHT]:
            self.x += 5
        if pressed_keys[K_LEFT]:
            self.x -= 5
        if pressed_keys[K_UP]:
            self.y -= 5
        if pressed_keys[K_DOWN]:
            self.y += 5
        if self.x >= 640:
            self.x = 1
        if self.x <= 0:
            self.x = 640
        if self.y <= 0:
            self.y = 479
        if self.y >= 480:
            self.y = 1

    def hit_by(self, raindrop):
        return pygame.Rect(self.x, self.y, 170, 192).collidepoint((raindrop.x, raindrop.y))
    def draw(self):
        screen.blit(mike_umbrella_image,(self.x, self.y))

"""Raindrop 클래스 정의"""
class Raindrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5, 18)
        self.bold = random.randint(1,4)

    def move(self):
        self.y += self.speed

    def off_screen(self):
        return self.y > 800

    def draw(self):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x, self.y+5), self.bold)

raindrops= []
mike = Mike()
cloud = Cloud()

while True:
    """게임 프레임 설정"""
    clock.tick(60)

    """종료시 프로그램 종료시키는 코드"""
    for event in pygame.event.get():
        pass
        if event.type == pygame.QUIT:
            sys.exit()



    """raindrop 실행"""
    i=0

    for i in range(random.randint(1, rain_quantity)):
        cloud.rain()

    screen.fill((255,255,255))

    mike.keydown()
    mike.draw()
    cloud.move()
    cloud.draw()

    """빗방울 그리기"""
    while i<len(raindrops):
        raindrops[i].move()
        raindrops[i].draw()
        if raindrops[i].off_screen() or mike.hit_by(raindrops[i]):
            del raindrops[i]
            i -= 1
        i+=1

    pygame.display.update()
