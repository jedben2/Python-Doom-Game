from ursina import *
from ursina import mouse
import numpy as np


class Gun(Entity):

    def attach(self, p):
        self.position = Vec2(p.x + 0.01, p.y)

    def __init__(self, p):
        super().__init__()
        self.model = 'quad'
        self.scale_y = .2
        self.attach(p)

    def look_at_mouse(self):
        relative_x, relative_y = self.screen_position.x, self.screen_position.y
        angle = np.arctan((mouse.y - relative_y) / (mouse.x - relative_x))
        self.rotation_z = -1 * (angle * 180 / np.pi)
        if mouse.x < relative_x:
            self.rotation_z -= 180


class Bullet(Entity):
    dt = 1 / 120

    def __init__(self, gun):
        super().__init__()
        self.model = 'quad'
        self.scale = .1
        self.rotation_z = gun.rotation_z
        self.position = Vec2(gun.x + 0.5 * np.cos(-1 * self.rotation_z * np.pi / 180),
                             gun.y + 0.5 * np.sin(-1 * self.rotation_z * np.pi / 180))

    def update(self):
        self.position += self.right * 5
        if self.x > 10 or self.x < -10: self.disable()