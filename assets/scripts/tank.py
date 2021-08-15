# tank
from ursina import *
import time
import numpy as np
import simpleaudio as sa
from assets.scripts import monster


class Tank(Entity):
    health = 10
    frame = 0
    direction = "left"
    dy = dx = 0
    dt = 1 / 120
    projectiles = []
    last_shot = time.time()
    dead = False

    def __init__(self, position):
        super().__init__(position=position,
                         model="quad")
        self.scale_x = 8
        self.scale_y = 5
        self.collider = SphereCollider(self, radius=.75)
        self.texture = "assets//animations//monsters//tank//left//0.png"
        self.f = Forcefield(self)

    def move(self, p, floor, camera):
        self.y -= 2

        self.position += Vec2(self.dx, self.dy)

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

        if self.health <= 0 and not self.dead:
            self.dead = True
            self.explosion = Explosion(self)
            self.collider = None

        if self.dead:
            self.explosion.animate_frames()
            if self.explosion.frame > 13 * 3:
                self.visible = self.f.visible = False
            if self.explosion.frame > 21 * 3:
                self.f.disable()
                self.explosion.cover.disable()
                self.explosion.disable()
                self.disable()

        self.y += 2

        self.f.attach(self)

        for projectile in self.projectiles:
            projectile.move(p)
            if not projectile.enabled: self.projectiles.remove(projectile)
        if time.time() - self.last_shot > 4 and not self.dead:
            self.projectiles.append(Projectile(self, random.randint(30, 60), random.randint(3, 6)))
            self.last_shot = time.time()

    def animate_frames(self):
        if self.dx != 0:
            if self.frame > 15:
                self.frame = 0
            if self.frame % 4 == 0:
                self.texture = f"assets//animations//monsters//tank//{self.direction}//{int(self.frame // 4)}.png"
        self.frame += 1
        self.f.animate_frames()
        for projectile in self.projectiles:
            projectile.animate_frames()


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


class Projectile(Entity):
    explosion = sa.WaveObject.from_wave_file("assets//sounds//explosion.wav")
    health = 6
    frame = 0
    dx = dy = 0
    dt = 1 / 120
    dead = False

    def __init__(self, tank, speed, rot_speed):
        super().__init__(model='quad')
        self.speed = speed
        self.rot_speed = rot_speed
        self.position = tank.position + Vec2(0, 1.1)
        self.scale = .4
        self.collider = 'box'

        if tank.direction == "left":
            self.rotation_z = -75
            self.x -= 2.3
        else:
            self.rotation_z = 75
            self.x += 2.3

    def move(self, player):
        if not self.dead and self.health <= 0:
            self.dead = True
            self.rotation_z = 0
            self.frame = 0
            self.scale *= 2
            self.collider = None
            # self.explosion.play()
        if self.dead:
            return
        origin_rotation = self.rotation_z
        self.look_at_2d(target=player)
        player_angle = self.rotation_z
        self.rotation_z = origin_rotation
        change_angle = player_angle - origin_rotation
        if change_angle < -180:
            change_angle += 360
        if change_angle > 180:
            change_angle -= 360
        self.rotation_z += np.sign(change_angle) * self.rot_speed
        self.position += self.up * self.dt * self.speed

    def animate_frames(self):
        if self.dead:
            if self.frame > 12:
                self.disable()
                return
            self.texture = f"assets//animations//monsters//tank//rocket//explosion//{self.frame}.png"
            self.frame += 1
            return

        self.texture = f"assets//animations//monsters//tank//rocket//{self.frame // 2}.png"
        self.frame += 1
        if self.frame == 4: self.frame = 0

class Explosion(Entity):
    frame = 0
    def __init__(self, tank):
        super().__init__(model='quad', scale=16)
        self.position = tank.position
        self.y += 2
    def animate_frames(self):
        self.texture = f"assets//animations//monsters//tank//death//{self.frame // 3}.png"
        if self.frame == 13 * 3:
            self.cover = ExplosionCover()
        self.frame += 1
        if self.frame == 21 * 3 + 2: self.disable()

class ExplosionCover(Entity):
    def __init__(self):
        super().__init__(model='quad', position=Vec2(0, 0), color=rgb(255, 166, 25, 255), scale=30)
        self.always_on_top = True
        self.fade_out(value=0, duration=1)