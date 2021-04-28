import pygame
import math
from pygame.locals import *

vec = pygame.math.Vector2

WIDTH = 640*2
HEIGHT = 480*2
TITLE = 'withpaint'
BLACK = (0,0,0)
YELLOW = (125, 125, 0)
WHITE = (255,255,255)
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
    def load_data(self):
        self.background = pygame.image.load('images/Stars.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def new(self):
        self.slither = Slither(self)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.slither.update()
        if self.slither.crash():
            self.playing = False

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
        self.draw_text(f"점수:{self.slither.score}  남은 시간: 스테이지",22, WHITE, WIDTH / 2, 15)
        pygame.display.update()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("위드 페인트 게임을 시작합니다. ", 22, WHITE, WIDTH / 2, HEIGHT / 2)
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
    def __init__(self, game):
        self.game = game
        self.pos= vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.data = [vec(WIDTH/2, HEIGHT/2), vec(WIDTH/2, HEIGHT/2), vec(WIDTH/2, HEIGHT/2)]
        self.score = START_SCORE
    def update(self):
        mouse = vec(pygame.mouse.get_pos())
        self.vel = self.pos - mouse
        self.vel = self.vel.normalize()
        self.pos -= self.vel*SLITHER_SPEED
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
            print(len(self.data)-self.data.index(i))
            if len(self.data)-self.data.index(i) > 10:
                crash = pygame.Rect(self.data[-1].x, self.data[-1].y, 10, 10).colliderect(pygame.Rect(i.x, i.y, 10,10))
                if crash == True:
                    return crash


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()