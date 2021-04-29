import random

import pygame
#import math
import sys
from pygame.locals import *

vec = pygame.math.Vector2

WIDTH = 640 * 3
HEIGHT = 480 * 2
TITLE = 'Slither'
BLACK = (0, 0, 0)
YELLOW = (125, 125, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60
SLITHER_SPEED = 5
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
        self.slither = Slither(self)
        self.pizzas = []
        self.spwntime = 0

    def load_data(self):
        self.background = pygame.image.load('images/Stars.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def new(self):
        self.slither = Slither(self)
        self.pizzas = []

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.slither.update()

        # 지렁이 충돌 확인
        if self.slither.crash():
            self.playing = False

        # 피자 생산
        if pygame.time.get_ticks() - self.spwntime > 1000 and len(self.pizzas) < 10:
            self.pizzas.append(Pizza(self))
            self.spwntime = pygame.time.get_ticks()

        # 지렁이가 피자 먹었는지 확인
        for i in self.pizzas:
            if self.slither.eat(i):
                self.pizzas.remove(i)
                self.slither.score += 50

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        self.pressed_keys = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 0))
        self.slither.draw()
        for i in self.pizzas:
            i.draw()
        self.draw_text(f"점수:{self.slither.score}  남은 시간: 스테이지", 22, WHITE, WIDTH / 2, 15)
        pygame.display.update()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("지렁이 게임을 시작합니다. ", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("스페이스키를 누루면 시작합니다. ", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("1, 2 :색 바꿈 설정         3, 4: 굵기 설정  esc: 지우기", 22, WHITE, WIDTH / 2, 15)
        pygame.display.update()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
        self.run()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(f'당신이 쏜 총알의 수는: ', 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f'당신의 점수는 : ', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f'당신의 빗나간 총알 수는 :', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text(f'다시 하고 싶으면 스페이스키를 누루세요.', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 50)
        self.draw_text(f'당신이 맞춘 수는 : ', 22, WHITE, WIDTH / 2, HEIGHT * 4 / 4 - 200)
        pygame.display.update()
        self.wait_for_key()
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
    def __init__(self, game_out):
        self.game = game_out
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.data = [vec(WIDTH / 2, HEIGHT / 2), vec(WIDTH / 2, HEIGHT / 2), vec(WIDTH / 2, HEIGHT / 2)]
        self.score = START_SCORE

    def update(self):
        mouse = vec(pygame.mouse.get_pos())
        self.vel = self.pos - mouse
        self.vel = self.vel.normalize()
        self.pos -= self.vel * SLITHER_SPEED
        pos = vec(self.pos.x, self.pos.y)
        self.data.append(pos)
        while len(self.data) > self.score:
            del self.data[0]

    def draw(self):
        for i in self.data:
            pygame.draw.circle(self.game.screen, YELLOW, i, 10)

    def crash(self):
        crash = False
        for i in self.data:
            if len(self.data) - self.data.index(i) > 10:
                crash = pygame.Rect(self.data[-1].x, self.data[-1].y, 10, 10).colliderect(pygame.Rect(i.x, i.y, 10, 10))
                if crash:
                    return crash

    def eat(self, pizza):
        return pygame.Rect(self.data[-1].x - 5, self.data[-1].y - 5, 10, 10).colliderect(
            pygame.Rect(pizza.pos.x - 20, pizza.pos.y - 20, 40, 40))


class Pizza:
    def __init__(self, game):
        self.game = game
        self.pos = vec(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.color = RED

    def draw(self):
        pygame.draw.circle(self.game.screen, self.color, self.pos, 40)


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()
