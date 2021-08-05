from ursina import *
from ursina import mouse


class Player(Entity):
    dy = 0
    dx = 0
    dt = 1 / 120
    jetpack = False
    direction = "right"
    airtime = 0
    health = 100
    frame = 0

    def __init__(self):
        super().__init__()
        self.scale_y = 1.5
        self.position = Vec2(0, 0)
        self.model = 'quad'
        # self.color = (255, 0, 0, 255)
        self.collider = 'box'
        self.texture = "assets//animations//player//move//right//0.png"

    def move(self, other):
        self.y -= .18
        self.dx = (held_keys['d'] - held_keys['a']) * self.dt * 20
        self.direction = "right"
        if mouse.x < self.screen_position.x: self.direction = "left"

        self.position += Vec2(self.dx, self.dy)

        if self.intersects(other).hit:
            self.y = 0
            if self.airtime > 0: self.airtime -= 2
            else: self.airtime = 0
        else:
            self.airtime += 1
            self.dy -= 9.81 * self.dt

        if self.dy < .25 and self.airtime < 75 and self.jetpack == True:
            self.dy += held_keys['w'] * 12 * self.dt
        else:
            self.jetpack = False
        if self.dy <= 0: self.jetpack = True
        self.y += .18

        if self.dx != 0:
            if self.dx > 0:
                if self.frame > 13:
                    self.frame = 0
                if self.frame % 1 == 0:
                    self.texture = f"assets//animations//player//move//right//{self.frame}.png"
                print(self.frame)
            elif self.dx < 0:
                if self.frame > 13:
                    self.frame = 0
                if self.frame % 1 == 0:
                    self.texture = f"assets//animations//player//move//left//{self.frame}.png"
                print(self.frame)
            self.frame += 1

    def update(self):
        pass
