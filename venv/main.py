import pygame, sys, random, time
from pygame.locals import *
pygame.init()
pygame.display.set_caption("비 맞는 마이크")
screen_x =640*2
screen_y =480*2

screen = pygame.display.set_mode((screen_x, screen_y))

clock = pygame.time.Clock()
raindrop_spawn_time = 0
last_hit_time = 0
rain_quantity=11 #구름 양

mike_umbrella_image = pygame.image.load("images/Mike_umbrella.png").convert()
mike_image = pygame.image.load(("images/mike.png")).convert()
cloud_image = pygame.image.load(("images/cloud.png")).convert()

"""구름 클래스 정의"""
class Cloud:
    def __init__(self, x):
        self.x = x
        self.y = 50
    def move(self):
        if self.x >= screen_x:
            self.x = 1
        self.x += 3
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
        if self.x >= screen_x:
            self.x = 1
        if self.x <= 0:
            self.x = screen_x
        if self.y <= 0:
            self.y = screen_y-1
        if self.y >= screen_y:
            self.y = 1

    def hit_by(self, raindrop):
        return pygame.Rect(self.x, self.y, 170, 192).collidepoint((raindrop.x, raindrop.y))
    def draw(self):
        if time.time() > last_hit_time+.1:
            screen.blit(mike_image, (self.x, self.y))
        else:
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
        return self.y > screen_y+20

    def draw(self):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x, self.y+5), self.bold)

raindrops= []
mike = Mike()
cloud = Cloud(50)
cloud2 = Cloud(screen_y/2)
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
        cloud2.rain()

    screen.fill((255,255,255))

    mike.keydown()
    mike.draw()
    cloud.move()
    cloud2.move()
    cloud.draw()
    cloud2.draw()

    """빗방울 그리기"""
    while i<len(raindrops):
        raindrops[i].move()
        raindrops[i].draw()
        flag = False
        if raindrops[i].off_screen():
            del raindrops[i]
            i -= 1
            flag = True
        if mike.hit_by(raindrops[i]):
            del raindrops[i]
            last_hit_time = time.time()
            i -= 1
            flag = True
        if flag:
            del raindrops[i]
            i -= 1
        i+=1

    pygame.display.update()
