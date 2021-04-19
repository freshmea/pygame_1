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

class Raindrop:
    def __init__(self):
        self.x = random.randint(0, 640)
        self.y = -5
        self.speed = random.randint(5, 18)

    def move(self):
        self.y += self.speed

    def off_screen(self):
        return self.y > 800

    def draw(self):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x, self.y+5), 1)
raindrops= []

while True:
    """게임 프레임 설정"""
    clock.tick(60)

    """종료시 프로그램 종료시키는 코드"""
    for event in pygame.event.get():
        pass
        if event.type == pygame.QUIT:
            sys.exit()

    """키 입력을 확인하고 움직임"""
    pressed_keys= pygame.key.get_pressed()
    if pressed_keys[K_RIGHT]:
        xpos += 5
    if pressed_keys[K_LEFT]:
        xpos -= 5
    if pressed_keys[K_UP]:
        ypos -= 5
    if pressed_keys[K_DOWN]:
        ypos += 5
    if xpos >= 640:
        xpos =1
    if xpos <= 0:
        xpos = 640
    if ypos <= 0:
        ypos = 479
    if ypos >= 480:
        ypos = 1

    """raindrop 실행"""
    i=0

    for i in range(random.randint(1, rain_quantity)):
        raindrops.append(Raindrop())

    screen.fill((255,255,255))

    while i<len(raindrops):
        raindrops[i].move()
        raindrops[i].draw()
        if raindrops[i].off_screen():
            del raindrops[i]
            i -= 1
        i+=1

    print(len(raindrops))
    pygame.draw.circle(screen, (0, 255, 0), (xpos, ypos), 20)
    pygame.display.update()
