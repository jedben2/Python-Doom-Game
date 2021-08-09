# Monsters
from ursina import *


class Monster(Entity):
    dx = dy = 0
    dt = 1 / 120
    attack_delay = 0
    max_delay = 0
    frame = 0
    direction = "right"

    def __init__(self, position):
        super().__init__(position=position,
                         model='quad')
        self.collider = 'box'

    def move(self, p, floor, camera):
        self.position += Vec2(self.dx, self.dy)

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

        if self.intersects(floor).hit:
            self.y = 0
        else:
            self.dy -= 9.81 * self.dt

        if self.health <= 0:
            self.disable()

    def animate_frames(self):
        if self.dx != 0:
            if self.frame > 21:
                self.frame = 0
            if self.frame % 2 == 0:
                self.texture = f"assets//animations//monsters//{self.speed}//{self.direction}//{int(self.frame // 2)}.png"
        self.frame += 1

    def attack(self, p, camera):
        if self.attack_delay < self.max_delay: self.attack_delay += 1
        if self.attack_delay == 10:
            self.attack_delay = 0
            p.health -= self.dmg

            if p.direction == "right": p.dx = -0.2
            else: p.dx = 0.2
            camera.shake(duration=0.05, magnitude=5)
        if self.attack_delay < 10: self.attack_delay += 1


class Small(Monster):
    def __init__(self, speed, position):
        super().__init__(position=position)

        self.max_delay = 5
        self.speed = speed
        self.scale = 1
        self.health = 30
        self.dmg = 1

        if self.speed == "run":
            self.scale = 1.2
            self.scale_x = 1
            self.dmg = 2

    def move(self, p, floor, camera):
        if self.speed == "walk":
            self.y += .05
        else:
            self.y += -.11

        Monster.move(self, p, floor, camera)

        if self.speed == "walk":
            self.y -= .05
        else:
            self.y -= -.11


class Medium(Monster):
    def __init__(self, speed, position):
        super().__init__(position=position)

        self.max_delay = 10
        self.speed = speed
        self.scale = 1.5
        self.health = 60
        self.dmg = 4

        if self.speed == "run":
            self.scale = 1.8
            self.scale_x = 1.6
            self.dmg = 8

    def move(self, p, floor, camera):
        if self.speed == "walk":
            self.y += -.19
        else:
            self.y += -.42

        Monster.move(self, p, floor, camera)

        if self.speed == "walk":
            self.y -= -.19
        else:
            self.y -= -.42


class Large(Monster):
    def __init__(self, speed, position):
        super().__init__(position=position)

        self.max_delay = 20
        self.speed = speed
        self.scale = 2
        self.health = 120
        self.dmg = 10

        if self.speed == "run":
            self.scale = 2.4
            self.scale_x = 1.8
            self.dmg = 14

    def move(self, p, floor, camera):
        if self.speed == "walk":
            self.y += -.42
        else:
            self.y += -.65

        Monster.move(self, p, floor, camera)

        if self.speed == "walk":
            self.y -= -.42
        else:
            self.y -= -.65
