# Game

from ursina import *
import player

app = Ursina()
window.vsync = 60
window.title = 'Doom Game'
window.borderless = False
window.fullscreen_size = (1920, 1080)
window.fullscreen = True
window.exit_button.visible = True
window.fps_counter.enabled = True

p = player.Player()
floor = Entity(model='quad', position=Vec2(0, -1), scale_x=50, collider='box')

camera.position = (p.x, p.y, -30)
camera.add_script(SmoothFollow(target=p, offset=[0, 0, -30], speed=10))

def update():
    p.move(floor)

app.run()