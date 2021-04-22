import pygame, sys, random, time, math
from pygame.locals import *


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
screen_x =640*2
screen_y =480*2
last_badguy_spawn_time = 0
font = pygame.font.Font(None, 25)
fighter_speed = 6
screen = pygame.display.set_mode((screen_x, screen_y))

badguy_image = pygame.image.load("images/badguy.png").convert()
badguy_image.set_colorkey((0, 0, 0))
fighter_image_1 = pygame.image.load("images/bat-a.png").convert()
fighter_image_2 = pygame.image.load("images/bat-b.png").convert()
fighter_image_3 = pygame.image.load("images/bat-c.png").convert()
fighter_image_1 = pygame.transform.scale(fighter_image_1,(100,59))
fighter_image_2 = pygame.transform.scale(fighter_image_2,(100,59))
fighter_image_3 = pygame.transform.scale(fighter_image_3,(100,59))
fighter_image_1.set_colorkey((0,0,0))
fighter_image_2.set_colorkey((0,0,0))
fighter_image_3.set_colorkey((0,0,0))

missile_image = pygame.image.load("images/missile.png").convert()
missile_image.set_colorkey((255,255,255))
GAME_OVER = pygame.image.load("images/gameover.png").convert()

background = pygame.image.load('images/Nebula.png')
background = pygame.transform.scale(background, (screen_x, screen_y))

missile_sound = pygame.mixer.Sound("sound/tank_hit.ogg")

class Fighter:
    def __init__(self):
        self.x =320
        self.y = screen_y-100
        self.shots = 0
        self.hits = 0
        self.misses = 0
        self.score = 0
    def move(self):
        if pressed_keys[K_LEFT] and self.x>0:
            self.x -= fighter_speed
        if pressed_keys[K_RIGHT] and self.x < screen_x-50:
            self.x += fighter_speed
        if pressed_keys[K_UP] and self.y>0:
            self.y -= fighter_speed
        if pressed_keys[K_DOWN] and self.x < screen_y-50:
            self.y += fighter_speed
    def fire(self):
        self.shots += 1
        missiles.append(Missile(self.x+50, self.y))
        missile_sound.play()

    def hit_by(self, badguy):
        return pygame.Rect(self.x, self.y, 100, 59).colliderect((badguy.x, badguy.y), (70, 45))
    def draw(self):
        if time.time() % 1 < 20/60:
            screen.blit(fighter_image_1, (self.x, self.y))
        elif time.time() % 1 < 40/60:
            screen.blit(fighter_image_2, (self.x, self.y))
        else :
            screen.blit(fighter_image_3, (self.x, self.y))



class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def move(self):
        self.y -= 5
    def off_screen(self):
        return self.y < -8
    def draw(self):
        #pygame.draw.line(screen, (255,0,0), (self.x, self.y),(self.x, self.y+8), 1)
        screen.blit(missile_image,(self.x-4, self.y))

class Badguy:
    def __init__(self):
        self.x = random.randint(0, screen_x-10)
        self.y = -100
        speed = random.randint(2,15)
        d = (math.pi)*random.random()-(math.pi/4)
        self.dx = math.sin(d)*speed
        self.dy = math.cos(d)*speed


    def move(self):
        o = random.randint(1, 1000)
        if o == 1:
            self.dx *= 2
        if o == 2:
            self.dy *= 2
        if o in range(3, 30):
            self.dy *= -1
        self.x += self.dx
        self.y += self.dy

    def touching(self,missile):
        return (self.x+35-missile.x)**2+(self.y+22-missile.y)**2<1225

    def bounce(self):
        if self.x<0 or self.x>screen_x-50:
            self.dx *= -1

    def draw(self):
        screen.blit(badguy_image,(self.x, self.y))

    def off_screen(self):
        return self.y >screen_y or self.y < -100

badguys = []
fighter = Fighter()
missiles = []

def setup():
    global badguys
    badguys = []
    global fighter
    fighter = Fighter()
    global missiles
    missiles = []

while True:
    clock.tick(60)


    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            fighter.fire()
    pressed_keys = pygame.key.get_pressed()

    if time.time() - last_badguy_spawn_time > 0.1:
        badguys.append(Badguy())
        last_badguy_spawn_time = time.time()

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    fighter.move()
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
            screen.blit(GAME_OVER, (170,200))

            screen.blit(font.render(str(fighter.shots), True, (255,255,255)), (266, 320))
            screen.blit(font.render(str(fighter.score), True, (255, 255, 255)), (266, 340))
            screen.blit(font.render(str(fighter.hits), True, (255, 255, 255)), (400, 320))
            screen.blit(font.render(str(fighter.misses), True, (255, 255, 255)), (400, 337))
            if fighter.shots ==0:
                screen.blit(font.render('---', True, (255, 255, 255)), (400, 357))
            else:
                screen.blit(font.render(str('{:.1f}%').format(100*fighter.hits/fighter.shots), True, (255, 255, 255)), (400, 357))
            while True:
                flag = 0
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_r:
                        flag = 1
                        break

                if flag == 1:
                    setup()
                    break
                pygame.display.update()

    for i in missiles:
        i.move()
        i.draw()
        if i.off_screen():
            missiles.remove(i)
            fighter.misses += 1

    screen.blit(font.render(f"Score: {fighter.score}", True, (255,255,255)),(5,5))
    pygame.display.update()
