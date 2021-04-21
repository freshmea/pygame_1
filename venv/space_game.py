import pygame, sys, random, time
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
screen_x =640*2
screen_y =480*2
last_badguy_spawn_time = 0
font = pygame.font.Font(None, 50)

screen = pygame.display.set_mode((screen_x, screen_y))

badguy_image = pygame.image.load("images/badguy.png").convert()
badguy_image.set_colorkey((0, 0, 0))
fighter_image = pygame.image.load("images/fighter.png").convert()
fighter_image.set_colorkey((255,255,255))
missile_image = pygame.image.load("images/missile.png").convert()
missile_image.set_colorkey((255,255,255))
GAME_OVER = pygame.image.load("images/gameover.png").convert()



class Fighter:
    shots = 0
    hits = 0
    misses = 0
    def __init__(self):
        self.x =320
    def move(self):
        if pressed_keys[K_LEFT] and self.x>0:
            self.x -= 3
        if pressed_keys[K_RIGHT] and self.x < screen_x-50:
            self.x += 3
    def fire(self):
        Fighter.shots += 1
        missiles.append(Missile(self.x+50))

    def hit_by(self, badguy):
        return ( badguy.y > screen_y-145 and badguy.y < screen_y-100 and badguy.x > self.x - 55 and badguy.x < self.x + 85 )
    def draw(self):
        screen.blit(fighter_image,(self.x, screen_y-100))

class Missile:
    def __init__(self, x):
        self.x = x
        self.y = screen_y-50
    def move(self):
        self.y -= 5
    def off_screen(self):
        return self.y < -8
    def draw(self):
        #pygame.draw.line(screen, (255,0,0), (self.x, self.y),(self.x, self.y+8), 1)
        screen.blit(missile_image,(self.x-4, self.y))

class Badguy:
    score = 0
    def __init__(self):
        self.x = random.randint(0, screen_x-10)
        self.y = -100
        self.dy = random.randint(2,6)
        self.dx = random.choice((-1,1))*self.dy

    def c_score(self):
        Badguy.score += 100

    def move(self):
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
        return self.y >screen_y


badguys = []
fighter = Fighter()
missiles = []

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            fighter.fire()
    pressed_keys = pygame.key.get_pressed()

    if time.time() - last_badguy_spawn_time > 0.5:
        badguys.append(Badguy())
        last_badguy_spawn_time = time.time()

    screen.fill((0,0,0))
    fighter.move()
    fighter.draw()

    for i in badguys:
        for j in missiles:
            if i.touching(j):
                i.c_score()
                Fighter.hits += 1
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

            screen.blit(font.render(str(Fighter.shots), True, (255,255,255)), (266, 320))
            screen.blit(font.render(str(Badguy.score), True, (255, 255, 255)), (266, 340))
            screen.blit(font.render(str(Fighter.hits), True, (255, 255, 255)), (400, 320))
            screen.blit(font.render(str(Fighter.misses), True, (255, 255, 255)), (400, 337))
            screen.blit(font.render(str(100*Fighter.hits/Fighter.shots), True, (255, 255, 255)), (400, 357))
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                pygame.display.update()

    for i in missiles:
        i.move()
        i.draw()
        if i.off_screen():
            missiles.remove(i)
            Fighter.misses += 1

    screen.blit(font.render(f"Score: {Badguy.score}", True, (255,255,255)),(5,5))
    pygame.display.update()
