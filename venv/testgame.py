import pygame, random, time, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1700, 960))
clock = pygame.time.Clock()
font = pygame.font.SysFont('malgungothic', 36)

charater_image = pygame.image.load("images/bat-a.png").convert()
charater_image.set_colorkey((0, 0, 0))
start_time = time.time()
x=0
y=0

while True:
    clock.tick(60)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pressed_keys = pygame.key.get_pressed()
    #3초 동안 방갑습니다. 출력하기
    if time.time() - start_time < 3:
        print(time.time() - start_time)
        a=font.render('방갑습니다!!!', True, (255, 255, 255))
        screen.blit(a, (200, 400))
    if pressed_keys[K_a]:
        x -= 1
    if pressed_keys[K_d]:
        x += 1
    if pressed_keys[K_w]:
        y -= 1
    if pressed_keys[K_s]:
        y += 1
    screen.blit(charater_image, (x*5, y*5))
    pygame.display.update()

