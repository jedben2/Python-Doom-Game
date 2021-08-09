# tank
from ursina import *
import time

class Tank(Entity):
    health = 1000
    dmg = 20
    attack_delay = 0
    frame = 0
    direction = 0
    dy = dx = 0
    dt = 1 / 120

    def __init__(self, position):
        super().__init__(position=position,
                         model="quad")
        self.scale_x = 8
        self.scale_y = 5
        self.collider = SphereCollider(self, radius=.75)
        self.texture = "assets//animations//monsters//tank//right//0.png"
        self.f = Forcefield(self)

    def move(self, p, floor, camera):
        self.y -= 2

        self.position += Vec2(self.dx, self.dy)

        # if self.intersects(p).hit:
        #     self.attack(p, camera)

        # else:
        if self.x > p.x:
            self.direction = "left"
            self.dx = -.01
        else:
            self.direction = "right"
            self.dx = .01

        if self.y < 0:
            self.y = 0
        else:
            self.dy -= 9.81 * self.dt

        if self.health <= 0:
            self.disable()

        self.y += 2

        # if self.direction == "right": self.model = "assets//animations//monsters//tank//right_tank.obj"
        # else: self.model = "assets//animations//monsters//tank//left_tank.obj"

        self.f.attach(self)

    def animate_frames(self):
        if self.dx != 0:
            if self.frame > 15:
                self.frame = 0
            if self.frame % 4 == 0:
                self.texture = f"assets//animations//monsters//tank//{self.direction}//{int(self.frame // 4)}.png"
        self.frame += 1
        self.f.animate_frames()
        # pass

    def attack(self, p, camera):
        if self.attack_delay < 100: self.attack_delay += 1
        if self.attack_delay == 100:
            self.attack_delay = 0
            p.health -= self.dmg

            if p.direction == "right": p.dx = -0.2
            else: p.dx = 0.2
            camera.shake(duration=0.05, magnitude=5)
        if self.attack_delay < 10: self.attack_delay += 1

class Forcefield(Entity):
    time_out = time_in = time.time()
    fade_time = .25
    frame = 0
    def __init__(self, tank):
        super().__init__()
        self.model = 'quad'
        self.attach(tank)
        self.scale_x = tank.scale_x * 1.5
        self.scale_y = tank.scale_y * 1.5
        self.texture = "assets//animations//monsters//tank//ffield//0.png"

    def attach(self, tank):
        self.position = tank.position
        self.y += 1.2

    def animate_frames(self):
        self.texture = f"assets//animations//monsters//tank//ffield//{self.frame}.png"
        self.frame += 1
        if self.frame == 5: self.frame = 0