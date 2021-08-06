# Monsters
from ursina import *


class Monster(Entity):
    dx = dy = 0
    dt = 1 / 120
    attack_delay = 10
    frame = 0

    def __init__(self, position, type, speed):
        super().__init__()
        self.model = 'quad'
        self.position = position
        self.collider = 'box'
        self.TYPE = type
        self.speed = speed
        if self.TYPE == "small":
            self.scale = 1
            self.health = 30
            if self.speed == "run":
                self.scale = 1.2
        elif self.TYPE == "medium":
            self.scale = 1.5
            self.health = 60
            if self.speed == "run":
                self.scale = 1.8
                self.scale_x = 1.6
        elif self.TYPE == "large":
            self.scale = 2
            self.health = 120

    def move(self, p, floor):
        if self.TYPE == "small": self.y += .05
        elif self.TYPE == "medium": self.y  += -.19
        self.dx = 0
        if self.intersects(p).hit:
            self.attack(p)
        else:
            if self.x > p.x:
                if self.speed == "walk":
                    self.dx = -.04
                else:
                    self.dx = -.13
            else:
                if self.speed == "walk":
                    self.dx = .04
                else:
                    self.dx = .13

        self.position += Vec2(self.dx, self.dy)

        if self.intersects(floor).hit:
            self.y = 0
        else:
            self.dy -= 9.81 * self.dt

        if self.attack_delay > 0: self.attack_delay -= 1

        if self.health <= 0:
            print("MONSTER DEAD")
            self.disable()

        if self.dx != 0:
            if self.dx > 0:
                self.direction = "right"
            else:
                self.direction = "left"

            if self.frame > 22:
                self.frame = 0
            if self.frame % 2 == 0:
                self.texture = f"assets//animations//monsters//1//{self.speed}//{self.direction}//{int(self.frame // 2)}.png"
        self.frame += 1

        if self.TYPE == "small":
            if self.speed == "walk":
                self.y -= .05
            else:
                self.y -= -.11
        elif self.TYPE == "medium":
            if self.speed == "walk":
                self.y -= -.19
            else:
                self.y -= -.42

    def attack(self, p):
        if self.attack_delay == 0:
            self.attack_delay = 10
            p.health -= 2
