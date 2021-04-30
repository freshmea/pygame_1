import abc
from abc import ABC

import pygame.math

vec =pygame.math.Vector2
class Camera:
    def __init__(self, player):
        self.player =player
        self.offset = vec(0,0)
        self.offset_float = vec(0,0)
        self.CONST = vec(0 ,0)

    def setmothod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abc.abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x = int(self.player.data[-1].x - self.camera.offset_float.x +self.camera.CONST.x) // 3
        self.camera.offset_float.y = int(self.player.data[-1].y - self.camera.offset_float.y +self.camera.CONST.y) // 3
        self.camera.offset.x, self.camera.offset.y = self.camera.offset_float.x, self.camera.offset_float.y
