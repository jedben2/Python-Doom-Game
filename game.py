# Game

from ursina import *
import player, gun
import numpy as np

app = Ursina()
window.vsync = 60
window.title = 'Doom Game'
window.borderless = False
window.fullscreen_size = (1920, 1080)
window.fullscreen = True
window.exit_button.visible = True
window.fps_counter.enabled = True

p = player.Player()
g = gun.Gun(p)
floor = Entity(model='quad', position=Vec2(0, -1), scale_x=50, collider='box')

airtime_counter = Text(text=str(p.airtime))
airtime_counter.scale = 3
airtime_counter.position = (.8, -.4)
camera.position = (p.x, p.y, -10)
camera.add_script(SmoothFollow(target=p, offset=[0, 0, -40], speed=10))

bullets = []

def update():
    p.move(floor)
    g.attach(p)
    g.look_at_mouse()
    if held_keys['left mouse']: bullets.append(gun.Bullet(g))
    airtime_counter.text = str(int(np.floor(p.airtime)))

app.run()
