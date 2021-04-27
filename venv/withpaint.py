import pygame
from pygame.locals import *

WIDTH = 640*2
HEIGHT = 480*2
TITLE = 'withpaint'
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60


class Paint:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption(TITLE)
        self.load_data()
        self.background=self.backgrounds[0]
        self.pencil = Pencil(self)
        self.k=0

    def load_data(self):
        self.backgrounds = []
        self.fighters = []
        # fighter 이미지
        fighter_data = ["images/pngegg.png"]
        for i in fighter_data:
            self.fighter_image = pygame.image.load(i).convert_alpha()
            self.fighters.append(self.fighter_image)

        # 미사일 이미지
        self.missile_image = pygame.image.load("images/missile.png").convert_alpha()
        self.missile_image = pygame.transform.scale(self.missile_image, (20, 80))
        # 배경 이미지
        background_data = ['images/Nebula.png', 'images/Space.png', 'images/Stars.png', 'images/Space City 1.png',
                           'images/Galaxy.png', 'images/Underwater 2.png', 'images/Stripes.png']
        for i in background_data:
            self.background = pygame.image.load(i).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.backgrounds.append(self.background)
        # 배드가이 이미지
        self.badguy_image = pygame.image.load("images/pngwing.com.png").convert_alpha()

        # 미사일 사운드
        self.missile_sound = pygame.mixer.Sound("sound/synth_laser_03.ogg")
        self.die_sound = pygame.mixer.Sound("sound/retro_die_03.ogg")

    def new(self):
        pass

    def update(self):
        if self.pressed_keys[K_1] and self.k > 0:
            self.k -= 5
        if self.pressed_keys[K_2] and self.k < 255:
            self.k += 5
        if self.pressed_keys[K_3] and self.pencil.bold > 1:
            self.pencil.bold -= 1
        if self.pressed_keys[K_4] and self.pencil.bold < 50:
            self.pencil.bold += 1
        if self.pressed_keys[K_ESCAPE]:
            self.pencil.datas = []

    def run(self):
        #pygame.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        #pygame.mixer.music.fadeout(500)

    def events(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x<255 and y<255:
                    self.pencil.chang_color((x,y,self.k))
                else:
                    self.pencil.on = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.pencil.on = False
        self.pencil.update()
        self.pressed_keys = pygame.key.get_pressed()
        self.pencil.expos = self.pencil.pos

    def draw(self):
        self.screen.fill(BLACK)
        #self.screen.blit(self.background, (0, 0))
        self.pencil.draw()
        self.draw_color_circle()
        self.draw_text(f"색상환:{self.k} 펜 색상{self.pencil.color} 굵기 {self.pencil.bold} ", 22, WHITE, WIDTH / 2, 15)
        pygame.display.update()



    def show_start_screen(self):
        # 시작 화면
        # pygame.mixer.music.load('sound/01 - Opening.ogg')
        # pygame.mixer.music.play(loops=-1)
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
        # 게임오버/ 계속
        # pygame.mixer.music.load('sound/06 - Rebels Be.ogg')
        # pygame.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text(f'당신이 쏜 총알의 수는: ', 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f'당신의 점수는 : ', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f'당신의 빗나간 총알 수는 :', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text(f'다시 하고 싶으면 스페이스키를 누루세요.', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 50)
        self.draw_text(f'당신이 맞춘 수는 : ', 22, WHITE, WIDTH / 2, HEIGHT * 4 / 4 - 200)
        pygame.display.update()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

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

    def draw_color_circle(self):
        for i in range(256):
            for j in range(256):
                    pygame.draw.line(self.screen, (i,j,self.k), (i,j), (i,j), 1)


class Pencil:
    def __init__(self, game):
        self.game = game
        self.pos =(0,0)
        self.expos = (0,0)
        self.color = WHITE
        self.bold = 3
        self.datas = []
        self.on = False

    def draw(self):
        for i in self.datas:
            if i[3]>10:
                pygame.draw.circle(self.game.screen, i[0], i[2], i[3])
            pygame.draw.line(self.game.screen, i[0], i[1], i[2], i[3])

    def chang_color(self, colorkey):
        self.color=colorkey

    def update(self):
        self.pos = pygame.mouse.get_pos()
        if self.pos != self.expos and self.on:
            self.datas.append([self.color, self.expos, self.pos, self.bold])


game = Paint()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()