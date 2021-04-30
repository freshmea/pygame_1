import numpy as np                         # numpy 호출
from matplotlib import pyplot as plt       # matplotlib의 pyplot 모듈 호출
import pygame
import math
vec = pygame.Vector2

X= []
Y= []

a= vec(10, 10)
b= vec(20, 20)
c= b-a
c=c.normalize()
d=c.rotate(90)
e= c.rotate(-90)
#d= vec(a.x-math.sin(math.radians(c)), a.y+math.cos(math.radians(c)))
print(c, d)
print(a+d)

for i in a, b, c, d, e, a+c, a+d, a+e:
    X.append(i.x)
    Y.append(i.y)
plt.scatter(X, Y)

plt.show()