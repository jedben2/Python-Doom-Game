# Monsters
from ursina import *


class Monster(Entity):
    dx = dy = 0
    dt = 1 / 120
    attack_delay = 6
    frame = 0
    direction = "right"
    dmg = 1

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
                self.scale_x = 1
                self.dmg = 2

        elif self.TYPE == "medium":
            self.scale = 1.5
            self.health = 60
            self.dmg = 4
            if self.speed == "run":
                self.scale = 1.8
                self.scale_x = 1.6
                self.dmg = 8

        elif self.TYPE == "large":
            self.scale = 2
            self.health = 120
            self.dmg = 10

    def move(self, p, floor, camera):
        attacking = False

        if self.TYPE == "small": self.y += .05
        elif self.TYPE == "medium": self.y  += -.19

        if self.intersects(p).hit:
            self.attack(p, camera)

        # else:
        if self.x > p.x:
            self.direction = "left"
            if self.speed == "walk":
                self.dx = -.04
            else:
                self.dx = -.13
        else:
            self.direction = "right"
            if self.speed == "walk":
                self.dx = .04
            else:
                self.dx = .13

        self.position += Vec2(self.dx, self.dy)

        if self.intersects(floor).hit:
            self.y = 0
        else:
            self.dy -= 9.81 * self.dt

        if self.attack_delay < 10: self.attack_delay += 1

        if self.health <= 0:
            print("MONSTER DEAD")
            self.disable()

        if self.dx != 0:
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

    def attack(self, p, camera):
        if self.attack_delay == 10:
            self.attack_delay = 0
            p.health -= self.dmg

            if p.direction == "right":
                p.dx = -0.3
            else:
                p.dx = 0.3
            camera.shake(duration=0.05, magnitude=10)
