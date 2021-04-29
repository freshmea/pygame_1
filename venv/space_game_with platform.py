from os import path

import math
import pygame
import random
import sys
import time
from pygame.locals import *

vec = pygame.math.Vector2

WIDTH = 640 * 2
HEIGHT = 480 * 2
last_badguy_spawn_time = 0
FPS = 60
TITLE = "Space Invaders"
BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
fighter_speed = 10
bullet_speed = 20
badguy_speed = 15
GAME_LIMITETIME = 69


def get_image(oimage, x, y, width, height):
    image = pygame.Surface((width, height))
    image.blit(oimage, (0, 0), pygame.Rect(x, y, width, height))
    image.set_colorkey(BLACK)

    return image


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption(TITLE)

        self.load_data()

    def load_data(self):
        self.backgrounds = []
        self.fighters = []
        self.dir = path.dirname(__file__)
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
        self.stage = 0
        self.score = 0
        self.badguys = []
        self.fighter = Fighter(self)
        self.missiles = []
        self.start_time = pygame.time.get_ticks()
        pygame.mixer.music.load("sound/03 - HWV 56 - Why do the nations so furiously rage together.ogg")
        pygame.mixer.music.play(-1)
        self.run()

    def run(self):
        pygame.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def update(self):
        # 스테이지 업데이트
        if (pygame.time.get_ticks() - self.start_time) / 10000 - self.stage > 0:
            self.stage += 1
            self.background = self.backgrounds[self.stage - 1]
            if self.stage == 3:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sound/04 - Sanctuary.ogg")
                pygame.mixer.music.play(-1)
        # 스프라이트 업데이트
        self.fighter.update()
        for i in self.badguys:
            i.update()
            if i.off_screen():
                self.badguys.remove(i)
        for i in self.missiles:
            i.update()
            if i.off_screen():
                self.missiles.remove(i)
                self.fighter.misses += 1

        # 배드가이 스폰
        global last_badguy_spawn_time
        if time.time() - last_badguy_spawn_time > 0.4 - self.stage / 30:
            self.badguys.append(Badguy(self))
            last_badguy_spawn_time = time.time()

        # 미사일 맞는 적
        for i in self.badguys:
            for j in self.missiles:
                if i.touching(j):
                    self.fighter.score += 100
                    self.fighter.hits += 1
                    self.badguys.remove(i)
                    self.missiles.remove(j)
                    self.die_sound.play()
                    break

        # 파이터가 적에 맞음
        for i in self.badguys:
            if self.fighter.hit_by(i):
                self.playing = False

        # 시간 초과
        if (pygame.time.get_ticks() - self.start_time) / 1000 > GAME_LIMITETIME:
            self.playing = False
            print(self.stage)

    def events(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.fighter.fire()
        self.pressed_keys = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, (0, 0))
        self.fighter.draw()
        for i in self.badguys, self.missiles:
            for j in i:
                j.draw()
        self.draw_text(
            f"점수: {self.fighter.score} 남은 시간:{GAME_LIMITETIME - (pygame.time.get_ticks() - self.start_time) / 1000:.2f} 스테이지 {self.stage}",
            22, WHITE, WIDTH / 2, 15)
        pygame.display.update()

    def show_start_screen(self):
        # 시작 화면
        pygame.mixer.music.load(path.join(self.dir, 'sound/01 - Opening.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("w 는 위로, s 는 아래로, a 는 왼쪽, d 는 오른쪽, 마우스 클릭이 미사일 발사 입니다.", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("스페이스키를 누루면 시작합니다. ", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("방갑습니다. 이제 게임을 시작합니다.", 22, WHITE, WIDTH / 2, 15)
        pygame.display.update()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def show_go_screen(self):
        # 게임오버/ 계속
        pygame.mixer.music.load(path.join(self.dir, 'sound/06 - Rebels Be.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill((0, 0, 0))
        if self.stage == 7:
            self.draw_text(f'당신은 모든 게임을 클리어 했습니다!!{self.stage} 성공!!', 48, WHITE, WIDTH / 2, HEIGHT / 4 - 100)
        self.draw_text(f'당신이 쏜 총알의 수는: {self.fighter.shots}', 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f'당신의 점수는 : {self.fighter.score}', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f'당신의 빗나간 총알 수는 :{self.fighter.misses}', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text(f'다시 하고 싶으면 스페이스키를 누루세요.', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 100)
        self.draw_text(f'당신이 맞춘 수는 : {self.fighter.hits}', 22, WHITE, WIDTH / 2, HEIGHT * 4 / 4 - 200)
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


class Fighter:
    def __init__(self, out_game):
        self.x = 320
        self.y = HEIGHT - 100
        self.dir = vec(0, 0)
        self.shots = 0
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.game = out_game
        self.load_image()
        self.image = self.image_frame[0]
        self.current_frame = 0
        self.last_update = 0

    def load_image(self):
        self.image_frame = []
        for i in range(5):
            for j in range(5):
                self.image_frame.append(get_image(self.game.fighters[0], i * 200, j * 200 + 50, 200, 100))
        for k, i in enumerate(self.image_frame):
            self.image_frame[k] = pygame.transform.scale(i, (200, 100))

    def update(self):
        self.set_dir()
        self.animate()
        self.move()

    def animate(self):
        now = pygame.time.get_ticks()
        if self.game.pressed_keys[K_a]:
            self.image = self.image_frame[2]
        elif self.game.pressed_keys[K_d]:
            self.image = self.image_frame[22]
        elif self.game.pressed_keys[K_w]:
            self.image = self.image_frame[10]
        elif self.game.pressed_keys[K_s]:
            self.image = self.image_frame[14]
        else:
            self.image = self.image_frame[12]

    def set_dir(self):
        x, y = pygame.mouse.get_pos()
        self.dir = vec(x - self.x, y - self.y)
        self.dir = self.dir / self.dir.length()

    def move(self):
        if self.game.pressed_keys[K_a] and self.x > 0:
            self.x -= fighter_speed
        if self.game.pressed_keys[K_d] and self.x < WIDTH - self.image.get_width():
            self.x += fighter_speed
        if self.game.pressed_keys[K_w] and self.y > 0:
            self.y -= fighter_speed
        if self.game.pressed_keys[K_s] and self.y < HEIGHT - self.image.get_height():
            self.y += fighter_speed

    def fire(self):
        self.shots += 1
        self.game.missiles.append(Missile(self.game, self.x + self.image.get_width() / 2, self.y, self.dir))
        self.game.missile_sound.play()

    def hit_by(self, badguy):
        fighter_rect = self.image.get_rect(left=self.x, top=self.y)
        badguy_rect = badguy.image.get_rect(left=badguy.x, top=badguy.y)
        return fighter_rect.collidepoint(badguy_rect.center)

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))


class Missile:
    def __init__(self, game, x, y, dir):
        self.speed = bullet_speed
        self.x = x
        self.y = y
        self.dir = dir
        self.game = game
        self.image = self.game.missile_image
        self.image = pygame.transform.rotate(self.image, self.dir.angle_to(vec(0, 0)) - 90)

    def update(self):
        self.move()
        self.animate()

    def animate(self):
        pass

    def move(self):
        self.y += self.speed * self.dir.y
        self.x += self.speed * self.dir.x

    def off_screen(self):
        return self.y < -8 or self.y > HEIGHT or self.x < -8 or self.x > WIDTH

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))


class Badguy:
    def __init__(self, game):
        self.x = random.randint(0, WIDTH - 10)
        self.y = -100
        speed = random.randint(2, badguy_speed)
        self.d = vec(random.randint(-5, 5), random.randint(0, 5))
        if self.d.length() != 0:
            self.d.normalize()
        self.dir = math.radians(self.d.angle_to(vec(0, 0)))
        self.dx = self.d.x * speed
        self.dy = self.d.y * speed
        self.game = game
        self.type = random.randint(1, self.game.stage)
        self.load_images()
        self.image = self.image_frame[0]
        self.last_update = 0
        self.current_frame = 0

    def load_images(self):
        self.image_frame = [get_image(self.game.badguy_image, 0, 0, 500, 500),
                            get_image(self.game.badguy_image, 540, 0, 500, 500),
                            get_image(self.game.badguy_image, 1000, 0, 500, 500)]
        for k, i in enumerate(self.image_frame):
            self.image_frame[k] = pygame.transform.scale(i, (100, 100))

    def update(self):
        self.animate()
        self.move()
        self.bounce()

    def move(self):

        if self.type == 1:
            speed = random.randint(2, badguy_speed)
            self.dy = speed / 2
            self.x += random.randint(5, 10) * math.sin(self.y / HEIGHT * 10)
            self.y += self.dy
        if self.type == 2:
            speed = badguy_speed
            self.dir += math.pi / 50
            self.dx = math.sin(self.dir) * speed
            self.dy = math.cos(self.dir) * speed
            self.x += self.dx
            self.y += self.dy + 5
        if self.type == 3:
            speed = random.randint(10, badguy_speed + 5)
            self.d = vec(self.game.fighter.x - self.x, self.game.fighter.y - self.y)
            if self.d.length() != 0:
                self.d = self.d / self.d.length()
            self.dx = self.d.x * speed / 3
            self.dy = self.d.y * speed / 3
            self.x += self.dx
            self.y += self.dy
        if self.type == 4:
            self.x += self.dx / 2
            self.y += self.dy / 2

    def touching(self, missile):
        badguy_rect = self.image.get_rect(left=self.x, top=self.y)
        badguy_rect.w *= 0.5
        badguy_rect.h *= 0.5
        badguy_rect.x += badguy_rect.w
        badguy_rect.y += badguy_rect.h
        missile_rect = self.game.missile_image.get_rect(left=missile.x, top=missile.y)
        return badguy_rect.colliderect(missile_rect)

    def bounce(self):
        if self.x < 0 or self.x > WIDTH - 50:
            self.dx *= -1

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame > 2:
                self.current_frame = 0
            self.image = self.image_frame[self.current_frame]
        if self.type == 3:
            x = int(100 * (0.5 + (now % 1000) / 1000))
            y = int(100 * (0.5 + (now % 1000) / 1000))
            self.image = pygame.transform.scale(self.image, (x, y))

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT or self.y < -100


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()

# https://opengameart.org/
# https://wikidocs.net/66237
