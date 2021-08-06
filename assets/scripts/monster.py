# Monsters
from ursina import *


class Monster(Entity):
    dx = dy = 0
    dt = 1 / 120
    attack_delay = 10
    frame = 0

    def __init__(self, position, type):
        super().__init__()
        self.model = 'quad'
        self.position = position
        self.collider = 'box'
        if type == "small":
            self.scale = 1
            self.health = 10
        elif type == "medium":
            self.health = 20
        elif type == "large":
            self.health = 40
        print(self.health)

    def move(self, p, floor):
        self.y += .05
        self.dx = 0
        if self.intersects(p).hit:
            self.attack(p)
        else:
            if self.x > p.x:
                self.dx = -.04
            else:
                self.dx = .04

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

            if self.frame > 33:
                self.frame = 0
            if self.frame % 3 == 0:
                self.texture = f"assets//animations//monsters//1//walk//{self.direction}//{int(self.frame // 3)}.png"
        self.frame += 1
        self.y -= .05

    def attack(self, p):
        if self.attack_delay == 0:
            self.attack_delay = 10
            p.health -= 2
