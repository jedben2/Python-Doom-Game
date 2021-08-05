# Gun + Bullets
from ursina import *
from ursina import mouse
import numpy as np


class Gun(Entity):

    def attach(self, p):
        self.position = Vec2(p.x + 0.3, p.y)

    def __init__(self, p):
        super().__init__()
        self.model = 'quad'
        self.scale_y = .1
        self.scale_x = .1
        self.attach(p)
        self.visible = False

    def look_at_mouse(self):
        relative_x, relative_y = self.screen_position.x, self.screen_position.y
        angle = np.arctan((mouse.y - relative_y) / (mouse.x - relative_x))
        self.rotation_z = -1 * (angle * 180 / np.pi)
        if mouse.x < relative_x:
            self.rotation_z -= 180
            self.x -= 0.6


class Bullet(Entity):
    dt = 1 / 120

    def __init__(self, gun):
        super().__init__()
        self.model = 'quad'
        self.scale = .1
        self.rotation_z = gun.rotation_z + random.randrange(-400, 401) / 100
        self.position = Vec2(gun.x + 0.1 * np.cos(-1 * self.rotation_z * np.pi / 180),
                             gun.y + 0.5 * np.sin(-1 * self.rotation_z * np.pi / 180))
        self.collider = 'box'

    def travel(self, monsters, floor):
        self.position += self.right * 3
        if self.x > 100 or self.x < -100: self.disable()
        for monster in monsters:
            if self.intersects(monster).hit:
                monster.health -= 1
                self.disable()
        if self.intersects(floor).hit:
            self.disable()
