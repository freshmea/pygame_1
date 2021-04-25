import pygame, sys, random, time, math
from pygame.locals import *

WIDTH = 640 * 2
HEIGHT = 480 * 2
last_badguy_spawn_time = 0
font = pygame.font.SysFont('malgungothic', 36)

fighter_speed = 6
bullet_speed = 10
badguy_speed = 15

start_time = 0


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Space Invaders")

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'images')
        self.fighter_image = pygame.image.load("images/bat-a.png").convert()
        fighter_image_1 = pygame.image.load("images/bat-a.png").convert()
        fighter_image_2 = pygame.image.load("images/bat-b.png").convert()
        fighter_image_3 = pygame.image.load("images/bat-c.png").convert()
        fighter_image_1 = pygame.transform.scale(fighter_image_1, (200, 100))
        fighter_image_2 = pygame.transform.scale(fighter_image_2, (200, 100))
        fighter_image_3 = pygame.transform.scale(fighter_image_3, (200, 100))
        fighter_image_1.set_colorkey((0, 0, 0))
        fighter_image_2.set_colorkey((0, 0, 0))
        fighter_image_3.set_colorkey((0, 0, 0))
        missile_image = pygame.image.load("images/missile.png").convert()
        missile_image = pygame.transform.scale(missile_image, (20, 80))
        missile_image.set_colorkey((255, 255, 255))
        background = pygame.image.load('images/Nebula.png').convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        missile_sound = pygame.mixer.Sound("sound/synth_laser_03.ogg")

    def new(self):
        self.score = 0
        self.badguys = []
        self.fighter = Fighter()
        self.missiles = []
        self.start_time = time.time()
        self.background_music = pygame.mixer.music.load("sound/01 - Opening.ogg")
        self.pygame.mixer.music.play(-1)
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
        pass

    def events(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                fighter.fire()
        pressed_keys = pygame.key.get_pressed()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


class Fighter:
    def __init__(self):
        self.x = 320
        self.y = HEIGHT - 100
        self.dir = 0
        self.shots = 0
        self.hits = 0
        self.misses = 0
        self.score = 0

    def set_dir(self):
        x, y = pygame.mouse.get_pos()
        self.dir = math.atan2(x - self.x, y - self.y) - math.pi / 2

    def move(self):
        if pressed_keys[K_a] and self.x > 0:
            self.x -= fighter_speed
        if pressed_keys[K_d] and self.x < WIDTH - fighter_image_1.get_width():
            self.x += fighter_speed
        if pressed_keys[K_w] and self.y > 0:
            self.y -= fighter_speed
        if pressed_keys[K_s] and self.y < HEIGHT - fighter_image_1.get_height():
            self.y += fighter_speed

    def fire(self):
        self.shots += 1
        missiles.append(Missile(self.x + fighter_image_1.get_width() / 2, self.y, self.dir))
        missile_sound.play()

    def hit_by(self, badguy):
        fighter_rect = fighter_image_1.get_rect(left=self.x, top=self.y)
        badguy_rect = badguy.image.get_rect(left=badguy.x, top=badguy.y)
        if fighter_rect.collidepoint(badguy_rect.center):
            print(fighter_rect, badguy_rect, badguy_rect.center)
        return fighter_rect.collidepoint(badguy_rect.center)

    def draw(self):
        rotated_1 = pygame.transform.rotate(fighter_image_1, self.dir)
        rotated_2 = pygame.transform.rotate(fighter_image_2, self.dir)
        rotated_3 = pygame.transform.rotate(fighter_image_3, self.dir)
        if time.time() % 1 < 20 / 60:
            screen.blit(rotated_1, (self.x, self.y))
        elif time.time() % 1 < 40 / 60:
            screen.blit(rotated_2, (self.x, self.y))
        else:
            screen.blit(rotated_3, (self.x, self.y))


class Missile:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def move(self):
        self.y -= bullet_speed * math.sin(self.dir)
        self.x += bullet_speed * math.cos(self.dir)

    def off_screen(self):
        return self.y < -8 or self.y > HEIGHT or self.x < -8 or self.x > WIDTH

    def draw(self):
        # pygame.draw.line(screen, (255,0,0), (self.x, self.y),(self.x, self.y+8), 1)
        screen.blit(missile_image, (self.x, self.y))


class Badguy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 10)
        self.y = -100
        speed = random.randint(2, badguy_speed)
        self.d = (math.pi) * random.random() - (math.pi / 4)
        self.dx = math.sin(self.d) * speed
        self.dy = math.cos(self.d) * speed
        self.type = random.randint(1, 3)
        self.image = pygame.image.load("images/badguy.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.rimage = pygame.transform.rotate(self.image, self.d)

    def move(self):
        o = random.randint(1, 1000)
        if o in range(1, 100):
            self.type = 1
        if o in range(100, 200):
            self.type = 2
        if o in range(200, 300):
            self.type = 3

        if self.type == 1:
            speed = random.randint(2, badguy_speed)
            self.dx = math.sin(self.d) * speed
            self.dy = math.cos(self.d) * speed
            self.x += self.dx
            if self.dy < 0:
                self.dy *= -1
            self.y += self.dy
        if self.type == 2:
            speed = badguy_speed + 5
            self.d += math.pi / 10
            self.dx = math.sin(self.d) * speed
            self.dy = math.cos(self.d) * speed
            self.x += self.dx
            self.y += self.dy
        if self.type == 3:
            speed = random.randint(10, badguy_speed + 5)
            self.dx = math.sin(self.d) * speed
            self.dy = math.cos(self.d) * speed
            if self.dy < 0:
                self.dy *= -1
            self.x += self.dx
            self.y += self.dy

    def touching(self, missile):
        badguy_rect = self.image.get_rect(left=self.x, top=self.y)
        missile_rect = missile_image.get_rect(left=missile.x, top=missile.y)
        return badguy_rect.colliderect(missile_rect)

    def bounce(self):
        if self.x < 0 or self.x > WIDTH - 50:
            self.dx *= -1

    def draw(self):
        self.rimage = pygame.transform.rotate(self.image, math.degrees(random.random() * math.pi))
        screen.blit(self.rimage, (self.x + self.rimage.get_width() / 2, self.y + self.rimage.get_height() / 2))

    def off_screen(self):
        return self.y > HEIGHT or self.y < -100


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()


def ending():
    ending_music = pygame.mixer.music.load("sound/06 - Rebels Be.ogg")
    pygame.mixer.music.play()
    screen.fill((0, 0, 0))
    screen.blit(font.render(f'당신이 쏜 총알의 수는: {fighter.shots}', True, (255, 255, 255)), (WIDTH / 4, HEIGHT / 4))
    screen.blit(font.render(f'당신의 점수는 : {fighter.score}', True, (255, 255, 255)), (WIDTH / 4, HEIGHT / 4 + 50))
    screen.blit(font.render(f'당신이 맞춘 수는 : {fighter.hits}', True, (255, 255, 255)), (WIDTH / 4, HEIGHT / 2))
    screen.blit(font.render(f'당신의 빗나간 총알 수는 :{fighter.misses}', True, (255, 255, 255)),
                (WIDTH / 4, HEIGHT / 2 + 50))
    if fighter.shots == 0:
        screen.blit(font.render('---', True, (255, 255, 255)), (400, 357))
    else:
        screen.blit(font.render(f'당신의 적중률은 :{100 * fighter.hits / fighter.shots:.2f}', True, (255, 255, 255)),
                    (WIDTH / 4, HEIGHT / 2 + 120))
    screen.blit(font.render(f'다시 하고 싶으면 스페이스 키를 누루세요.', True, (255, 255, 255)),
                (WIDTH / 4, HEIGHT / 2 + 160))
    while True:
        flag = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                flag = 1
                break

        if flag == 1:
            start()
            break
        pygame.display.update()


start()

while True:

    if time.time() - last_badguy_spawn_time > 0.2:
        badguys.append(Badguy())
        last_badguy_spawn_time = time.time()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    fighter.move()
    fighter.set_dir()
    fighter.draw()

    for i in badguys:
        for j in missiles:
            if i.touching(j):
                fighter.score += 100
                fighter.hits += 1
                badguys.remove(i)
                missiles.remove(j)
                break
        i.move()
        i.bounce()
        i.draw()
        if i.off_screen():
            badguys.remove(i)

    for i in badguys:
        if fighter.hit_by(i):
            ending()

    for i in missiles:
        i.move()
        i.draw()
        if i.off_screen():
            missiles.remove(i)
            fighter.misses += 1
    if time.time() - start_time > 10:
        ending()
    screen.blit(font.render(f"점수: {fighter.score} 남은 시간:{10 - (time.time() - start_time):.2f}", True, (255, 255, 255)),
                (5, 5))
    pygame.display.update()

# https://opengameart.org/
# https://wikidocs.net/66237