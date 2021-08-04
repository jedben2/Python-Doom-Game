# Game
from ursina.prefabs.health_bar import HealthBar
from ursina import *
import player, gun, monster
import numpy as np

app = Ursina()
window.vsync = 60
window.title = 'Doom Game'
window.borderless = False
window.fullscreen_size = (1920, 1080)
window.fullscreen = True
window.exit_button.visible = True

p = player.Player()
p_healthbar = HealthBar(value=p.health)
p_healthbar.position = Vec2(-.15 / 2, .15/2)
p_healthbar.scale_x = .15


g = gun.Gun(p)
floor = Entity(model='quad', position=Vec2(0, -1), scale_x=50, collider='box')
m = monster.Monster(position=Vec2(-10, 0), type="small")

airtime_counter = Text(text=str(p.airtime))
airtime_counter.scale = 3
airtime_counter.position = (.8, -.4)
camera.position = (p.x, p.y, -10)
camera.add_script(SmoothFollow(target=p, offset=[0, 0, -40], speed=20))

bullets = []

def update():
    p.move(floor)
    m.move(p, floor)
    g.attach(p)
    g.look_at_mouse()
    if held_keys['left mouse']: bullets.append(gun.Bullet(g))
    for bullet in bullets:
        if bullet.enabled == False: bullets.remove(bullet)
    airtime_counter.text = str(int(np.floor(p.airtime)))
    p_healthbar.value = p.health


app.run()
