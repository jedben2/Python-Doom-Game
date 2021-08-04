from ursina import *


class Monster(Entity):
    dx = dy = 0
    dt = 1 / 120
    attack_delay = 10

    def __init__(self, position, type):
        super().__init__()
        self.model = 'quad'
        self.position = position
        self.collider = 'box'
        if type == "small":
            self.scale = 1

    def move(self, p, floor):
        self.dx = 0
        if self.intersects(p).hit:
            self.attack(p)
        else:
            if self.x > p.x:
                self.dx = -.06
            else:
                self.dx = .06

        self.position += Vec2(self.dx, self.dy)

        if self.intersects(floor).hit:
            self.y = 0
        else:
            self.dy -= 9.81 * self.dt

        if self.attack_delay > 0: self.attack_delay -= 1

    def attack(self, p):
        if self.attack_delay == 0:
            self.attack_delay = 10
            p.health -= 1
        print(p.health)