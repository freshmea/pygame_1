import random

import pygame
import math
import sys
from pygame.locals import *
from camera import *

vec = pygame.math.Vector2

WIDTH = 640*2
HEIGHT = 480*2
TITLE = 'slither'

BLACK = (0,0,0)
YELLOW = (125, 125, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 30
SLITHER_SPEED = 10
START_SCORE = 100


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption(TITLE)
        self.load_data()
        self.slithers = []
        self.pizzas = []
        self.spwntime = 0



    def load_data(self):
        self.background = pygame.image.load('images/Stars.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH*3, HEIGHT*3))
        self.pizza_image = pygame.image.load('images/pizza.png').convert_alpha()
        self.pizza_image = pygame.transform.scale(self.pizza_image, (80, 80))

    def new(self):
        self.slithers = []
        self.pizzas = []

    def run(self):
        self.playing = True
        self.slithers.append(Slither(self,1))
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #지렁이 추가
        if len(self.slithers) < 20:
            self.slithers.append(Slither(self, 2))
        for i in self.slithers:
            i.update()

        #지렁이 충돌 확인
        for i in self.slithers:
            if self.slithers[0].crash(i):
                self.playing = False

        #지렁이들의 충돌 확인
        # for i in self.slithers[1:]:
        #     for j in self.slithers:
        #         if i.crash(j):
        #             try:
        #                 self.slithers.remove(i)
        #             except:
        #                 pass


        # 피자 생산
        if pygame.time.get_ticks()-self.spwntime > 1000 and len(self.pizzas) < 10 :
            self.pizzas.append(Pizza(self))
            self.spwntime = pygame.time.get_ticks()

        #지렁이가 피자 먹었는지 확인
        for i in self.pizzas:
            for j in self.slithers:
                if j.eat(i):
                    self.pizzas.remove(i)
                    j.score += 50

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        self.pressed_keys = pygame.key.get_pressed()


    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0 - self.slithers[0].data[-1].x+WIDTH/2-WIDTH, 0 - self.slithers[0].data[-1].y+HEIGHT/2-HEIGHT))
        for i in self.slithers:
            i.draw(self.slithers[0].data[-1].x-WIDTH/2, self.slithers[0].data[-1].y-HEIGHT/2)
        for i in self.pizzas:
            i.draw(self.slithers[0].data[-1].x-WIDTH/2, self.slithers[0].data[-1].y-HEIGHT/2)
        self.draw_text(f"점수:{self.slithers[0].score}  남은 시간: 스테이지",22, WHITE, WIDTH / 2, 15)
        pygame.display.update()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("지렁이 게임을 시작합니다. ", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("스페이스키를 누루면 시작합니다. ", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("냐하하", 22, WHITE, WIDTH / 2, 15)
        pygame.display.update()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
        self.new()
        self.run()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(f'당신이 점수는: {self.slithers[0].score}', 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f'', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f'', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text(f'다시 하고 싶으면 스페이스키를 누루세요.', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 50)
        self.draw_text(f' ', 22, WHITE, WIDTH / 2, HEIGHT * 4 / 4 - 200)
        pygame.display.update()
        self.wait_for_key()
        self.new()
        self.run()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont('malgungothic', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

class Slither:
    def __init__(self, game, type: int):
        self.game = game
        self.pos= vec(random.randint( -WIDTH, WIDTH*2), random.randint(-HEIGHT, HEIGHT*2))
        self.vel = vec(0, 0)
        self.data = [vec(0, 0), vec(0, 0), vec(0, 0)]
        self.score = START_SCORE
        self.aidata = []
        for i in range(10):
            self.aidata.append((random.randint(-WIDTH,WIDTH*2), random.randint(-HEIGHT, HEIGHT*2)))
        self.beforeai = (0,0)
        self.spwntime1 = 0
        self.type = type
        self.color = random.choice([YELLOW, BLACK, WHITE, GREEN, RED, BLUE])
        self.data_poly = []

    def update(self):
        if self.type == 1:
            mouse = vec(pygame.mouse.get_pos())
            mouse = mouse - vec(-self.data[-1].x+WIDTH/2, -self.data[-1].y+HEIGHT/2)
        elif self.type == 2:
            mouse = vec(self.ai())
        self.vel = mouse - self.pos
        self.vel = self.vel.normalize()
        self.pos += self.vel*SLITHER_SPEED
        pos = vec(self.pos.x, self.pos.y)
        vel = self.vel
        self.data.append(pos)
        self.data_poly.append([pos,vel])
        while len(self.data) > self.score:
            del self.data[0]
            del self.data_poly[0]

    def draw(self, x, y):
        if self.type == 1:
            data_poly = []
            for i in self.data_poly:
                data_poly.append(i[0]+vec(20*i[1].rotate(90), 20*i[1].rotate(90))-vec(x,y))
            for i in self.data_poly[::-1]:
                data_poly.append(i[0]+vec(20*i[1].rotate(-90), 20*i[1].rotate(-90))-vec(x,y))
            if len(data_poly)>4:
                pygame.draw.polygon(self.game.screen, random.choice([YELLOW, BLACK, WHITE, GREEN, RED,BLUE]), data_poly)
        if self.type == 2 :
            data_poly = []
            for i in self.data_poly:
                data_poly.append(i[0]+vec(20*i[1].rotate(90), 20*i[1].rotate(90))-vec(x,y))
            for i in self.data_poly[::-1]:
                data_poly.append(i[0]+vec(20*i[1].rotate(-90), 20*i[1].rotate(-90))-vec(x,y))
            if len(data_poly) > 4:
                pygame.draw.polygon(self.game.screen, self.color,data_poly)

    def crash(self, badguy):
        crash = False
        if self.type == 2:
            if self.data == badguy.data:
                return False
        for i in badguy.data:
            if len(self.data)-badguy.data.index(i) > 4:
                crash = pygame.Rect(self.data[-1].x, self.data[-1].y, 20, 20).collidepoint((i.x, i.y))
                if crash == True:
                    return crash



    def eat(self, pizza):
        return pygame.Rect(self.data[-1].x-5, self.data[-1].y-5, 20, 20).colliderect(pygame.Rect(pizza.pos.x, pizza.pos.y, 80, 80))

    def ai(self):
        if pygame.time.get_ticks()-self.spwntime1 > 500 :
            self.beforeai = self.aidata[random.randint(0,3)]
            self.spwntime1=pygame.time.get_ticks()
            return self.beforeai
        else :
            return self.beforeai



class Pizza:
    def __init__(self, game):
        self.game = game
        self.pos = vec(random.randint( -WIDTH, WIDTH*2), random.randint(-HEIGHT, HEIGHT*2))

    def draw(self, x, y):
        self.game.screen.blit( self.game.pizza_image, self.pos-vec(x, y))







game = Game()
game.show_start_screen()
while game.running:
    game.show_go_screen()

pygame.quit()