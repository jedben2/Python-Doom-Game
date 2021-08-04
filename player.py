from ursina import *


class Player(Entity):
    dy = 0
    dx = 0
    dt = 1 / 120
    jetpack = False

    def __init__(self):
        super().__init__()
        self.position = Vec2(0, 1)
        self.model = 'quad'
        self.color = (255, 0, 0, 255)
        self.collider = 'box'

    def move(self, other):
        self.dx = (held_keys['d'] - held_keys['a']) * self.dt * 20
        self.position += Vec2(self.dx, self.dy)
        if self.y <= 0:
            self.y = 0
            self.jetpack = True
        else:
            self.dy -= 9.81 * self.dt
        if self.dy < .5 and self.jetpack:
            self.dy += held_keys['w'] * 15 * self.dt
        else:
            self.jetpack = False
