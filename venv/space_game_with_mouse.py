import pygame, sys, random, time, math
from pygame.locals import *


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
screen_x =640*2
screen_y =480*2
last_badguy_spawn_time = 0
font =pygame.font.SysFont('malgungothic', 36)

fighter_speed = 6
bullet_speed = 10
badguy_speed = 15
screen = pygame.display.set_mode((screen_x, screen_y))
start_time=0

badguy_image = pygame.image.load("images/frog.png").convert()
badguy_image = pygame.transform.scale(badguy_image, (100, 80))
badguy_image.set_colorkey((255, 255, 255))
fighter_image_1 = pygame.image.load("images/bat-a.png").convert()
fighter_image_2 = pygame.image.load("images/bat-b.png").convert()
fighter_image_3 = pygame.image.load("images/bat-c.png").convert()
fighter_image_1 = pygame.transform.scale(fighter_image_1,(200,100))
fighter_image_2 = pygame.transform.scale(fighter_image_2,(200,100))
fighter_image_3 = pygame.transform.scale(fighter_image_3,(200,100))
fighter_image_1.set_colorkey((0,0,0))
fighter_image_2.set_colorkey((0,0,0))
fighter_image_3.set_colorkey((0,0,0))

missile_image = pygame.image.load("images/missile.png").convert()
missile_image = pygame.transform.scale(missile_image, (20, 80))
missile_image.set_colorkey((255,255,255))

background = pygame.image.load('images/Nebula.png').convert()
background = pygame.transform.scale(background, (screen_x, screen_y))

missile_sound = pygame.mixer.Sound("sound/synth_laser_03.ogg")

class Fighter:
    def __init__(self):
        self.x =320
        self.y = screen_y-100
        self.dir = 0
        self.shots = 0
        self.hits = 0
        self.misses = 0
        self.score = 0

    def set_dir(self):
        x, y = pygame.mouse.get_pos()
        self.dir = math.atan2(x-self.x,y-self.y)-math.pi/2


    def move(self):
        if pressed_keys[K_a] and self.x > 0:
            self.x -= fighter_speed
        if pressed_keys[K_d] and self.x < screen_x-fighter_image_1.get_width():
            self.x += fighter_speed
        if pressed_keys[K_w] and self.y > 0:
            self.y -= fighter_speed
        if pressed_keys[K_s] and self.y < screen_y-fighter_image_1.get_height():
            self.y += fighter_speed
    def fire(self):
        self.shots += 1
        missiles.append(Missile(self.x+fighter_image_1.get_width()/2, self.y, self.dir))
        missile_sound.play()

    def hit_by(self, badguy):
        fighter_rect = fighter_image_1.get_rect(left=self.x, top=self.y)
        badguy_rect = badguy_image.get_rect(left=badguy.x, top=badguy.y)
        if fighter_rect.collidepoint(badguy_rect.center):
            print(fighter_rect, badguy_rect, badguy_rect.center)
        return fighter_rect.collidepoint(badguy_rect.center)

    def draw(self):
        rotated_1 = pygame.transform.rotate(fighter_image_1, self.dir)
        rotated_2 = pygame.transform.rotate(fighter_image_2, self.dir)
        rotated_3 = pygame.transform.rotate(fighter_image_3, self.dir)
        if time.time() % 1 < 20/60:
            screen.blit(rotated_1, (self.x, self.y))
        elif time.time() % 1 < 40/60:
            screen.blit(rotated_2, (self.x, self.y))
        else :
            screen.blit(rotated_3, (self.x, self.y))



class Missile:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
    def move(self):
        self.y -= bullet_speed*math.sin(self.dir)
        self.x += bullet_speed*math.cos(self.dir)
    def off_screen(self):
        return self.y < -8 or self.y > screen_y or self.x < -8 or self.x > screen_x
    def draw(self):
        #pygame.draw.line(screen, (255,0,0), (self.x, self.y),(self.x, self.y+8), 1)
        screen.blit(missile_image,(self.x, self.y))

class Badguy:
    def __init__(self):
        self.x = random.randint(0, screen_x-10)
        self.y = -100
        speed = random.randint(2,badguy_speed)
        self.d = (math.pi)*random.random()-(math.pi/4)
        self.dx = math.sin(self.d)*speed
        self.dy = math.cos(self.d)*speed
        self.type = 1


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
            speed = badguy_speed+5
            self.d += math.pi/10
            self.dx = math.sin(self.d) * speed
            self.dy = math.cos(self.d) * speed
            self.x += self.dx
            self.y += self.dy
        if self.type == 3:
            speed = random.randint(10, badguy_speed+5)
            self.dx = math.sin(self.d) * speed
            self.dy = math.cos(self.d) * speed
            if self.dy < 0:
                self.dy *= -1
            self.x += self.dx
            self.y += self.dy

    def touching(self,missile):
        badguy_rect=badguy_image.get_rect(left=self.x, top=self.y)
        missile_rect=missile_image.get_rect(left=missile.x, top=missile.y)
        return badguy_rect.collidepoint(missile_rect.centerx, missile_rect.centery)

    def bounce(self):
        if self.x<0 or self.x>screen_x-50:
            self.dx *= -1

    def draw(self):
        screen.blit(badguy_image,(self.x, self.y))

    def off_screen(self):
        return self.y >screen_y or self.y < -100



def start():
    global badguys
    badguys = []
    global fighter
    fighter = Fighter()
    global missiles
    missiles = []
    global start_time
    start_time=time.time()
    background_music = pygame.mixer.music.load("sound/01 - Opening.ogg")
    pygame.mixer.music.play(-1)

def ending():
    ending_music = pygame.mixer.music.load("sound/06 - Rebels Be.ogg")
    pygame.mixer.music.play()
    screen.fill((0, 0, 0))
    screen.blit(font.render(f'당신이 쏜 총알의 수는: {fighter.shots}', True, (255, 255, 255)), (screen_x / 4, screen_y / 4))
    screen.blit(font.render(f'당신의 점수는 : {fighter.score}', True, (255, 255, 255)), (screen_x / 4, screen_y / 4 + 50))
    screen.blit(font.render(f'당신이 맞춘 수는 : {fighter.hits}', True, (255, 255, 255)), (screen_x / 4, screen_y / 2))
    screen.blit(font.render(f'당신의 빗나간 총알 수는 :{fighter.misses}', True, (255, 255, 255)),
                (screen_x / 4, screen_y / 2 + 50))
    if fighter.shots == 0:
        screen.blit(font.render('---', True, (255, 255, 255)), (400, 357))
    else:
        screen.blit(font.render(f'당신의 적중률은 :{100 * fighter.hits / fighter.shots:.2f}', True, (255, 255, 255)),
                    (screen_x / 4, screen_y / 2 + 120))
    screen.blit(font.render(f'다시 하고 싶으면 스페이스 키를 누루세요.', True, (255, 255, 255)),
                (screen_x / 4, screen_y / 2 + 160))
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
    clock.tick(60)



    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            fighter.fire()
    pressed_keys = pygame.key.get_pressed()

    if time.time() - last_badguy_spawn_time > 0.2:
        badguys.append(Badguy())
        last_badguy_spawn_time = time.time()

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
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
    if time.time()-start_time> 10:
        ending()
    screen.blit(font.render(f"점수: {fighter.score} 남은 시간:{10-(time.time()-start_time):.2f}", True, (255,255,255)),(5,5))
    pygame.display.update()


#https://opengameart.org/