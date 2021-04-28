import pygame

size = width, height = 800, 600
win = pygame.display.set_mode(size)
bg = pygame.transform.rotozoom(pygame.image.load('Flat Nature Art.png'), 0, 0.85)
char1 = pygame.transform.rotozoom(pygame.image.load('png/Walk (1).png'), 0, 0.35)
char2 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (1).png'), True, False), 0, 0.35)

# win.fill((255,255,255))

win.blit(bg, (0, 0))
pygame.display.update()

pygame.init()
clock = pygame.time.Clock()

# Load an image

walkRight = [pygame.transform.rotozoom(pygame.image.load('png/Walk (1).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (2).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (3).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (4).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (5).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (6).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (7).png'), -5, 0.35),
             pygame.transform.rotozoom(pygame.image.load('png/Walk (8).png'), -5, 0.35)]

walkLeft = [
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (1).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (2).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (3).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (4).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (5).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (6).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (7).png'), True, False), 1, 0.35),
    pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('png/Walk (8).png'), True, False), 1, 0.35)]
print(walkLeft)

vel = 10
x = 50
y = 350
left = False
right = False
walkcount = 0
stopd = True


def redrawG():
    global walkcount

    win.blit(bg, (0, 0))
    # win.fill((255, 255, 255))

    if walkcount >= 32:
        walkcount = 0

    # walk right
    if right:
        win.blit(walkRight[walkcount // 4], (x, y))
        print(walkcount // 4)
        walkcount += 1
    # walk left
    elif left:
        win.blit(walkLeft[walkcount // 4], (x, y))
        walkcount += 1

    elif stopd:
        win.blit(char1, (x, y))
        print("Right Direction")
    else:
        win.blit(char2, (x, y))
        print("Left Direction")
        pass
    pygame.display.update()


run = True

while run:
    clock.tick(48)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYUP:
            if right:
                right = False
                stopd = True
            if left:
                left = False
                stopd = False
            pass

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        if x > width - 100:
            x = width - 100
        x += vel
        right = True
        left = False
    if keys[pygame.K_a]:
        if x < -150:
            x = -150
        x -= vel
        right = False
        left = True

    redrawG()

pygame.quit()


#https://www.gameart2d.com/free-dino-sprites.html
