# Player
from ursina import *
from ursina import mouse


class Player(Entity):
    dy = 0
    dx = 0
    dt = 1 / 120
    direction = "right"
    health = 100
    frame = 0

    def __init__(self):
        super().__init__()
        self.scale_y = 1.5
        self.position = Vec2(0, 0)
        self.model = 'quad'
        # self.color = (255, 0, 0, 255)
        self.collider = 'box'
        self.texture = "assets//animations//player//idle//right//0.png"

    def move(self, floor):
        self.y -= .18

        self.dx += (held_keys['d'] - held_keys['a']) * self.dt * 20 * (1 + held_keys['left shift']) * (
                1 - held_keys['left mouse']) * .1

        if self.dx != 0:
            if self.dx > (held_keys['d']) * self.dt * 20 * (1 + held_keys['left shift']) * (
                    1 - held_keys['left mouse']):
                self.dx = (held_keys['d']) * self.dt * 20 * (1 + held_keys['left shift']) * (
                        1 - held_keys['left mouse'])
            elif self.dx < (-1 * held_keys['a']) * self.dt * 20 * (1 + held_keys['left shift']) * (
                    1 - held_keys['left mouse']):
                self.dx = (-1 * held_keys['a']) * self.dt * 20 * (1 + held_keys['left shift']) * (
                        1 - held_keys['left mouse'])

        self.position += Vec2(self.dx, self.dy)

        if self.intersects(floor).hit:
            self.y = 0
            self.dy = held_keys['w'] * .65
        else:
            self.dy -= 9.81 * self.dt
        self.y += .18

        if self.dx != 0:
            if self.dx > 0:
                self.direction = "right"
            else:
                self.direction = "left"

            if self.frame > 13:
                self.frame = 0
            if self.frame % 1 == 0:
                self.texture = f"assets//animations//player//move//{self.direction}//{int(self.frame // 1)}.png"
        else:
            if self.frame > 9:
                self.frame = 0
            if self.frame % 3 == 0:
                self.texture = f"assets//animations//player//idle//{self.direction}//{self.frame // 3}.png"
        self.frame += 1

    def update(self):
        pass
