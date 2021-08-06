# Game
from ursina.prefabs.health_bar import HealthBar
from ursina import *
from assets.scripts import monster, gun, player

app = Ursina()
window.vsync = 60
window.title = 'Doom Game'
window.borderless = False
window.fullscreen_size = (1920, 1080)
window.fullscreen = True
window.exit_button.visible = True
window.fps_counter.visible = False

p = player.Player()
p_healthbar = HealthBar(value=p.health)
p_healthbar.position = Vec2(-.15 / 2, .15 / 2)
p_healthbar.scale_x = .15

g = gun.Gun(p)
floor = Entity(model='quad', position=Vec2(0, -1), scale_x=50, collider='box', texture='grass')

camera.position = (p.x, p.y, -10)
camera.add_script(SmoothFollow(target=p, offset=[0, 0, -25], speed=20))

bullets = []
monsters = []

monsters.append(monster.Monster(position=Vec2(-10, 0), type="small"))
monsters.append(monster.Monster(position=Vec2(10, 0), type="small"))

shot_time = 0

p_old_x, p_old_y = p.x, p.y

def update():
    global shot_time, p_old_y, p_old_x

    p.x, p.y = p_old_x, p_old_y
    p.scale_y = 1.5
    p.scale_x = 1

    shot_time += 1

    p.move(floor)

    p_old_x, p_old_y = p.x, p.y

    for monster in monsters:
        monster.move(p, floor)
        if monster.enabled == False: monsters.remove(monster)

    g.attach(p)
    g.look_at_mouse()

    for bullet in bullets:
        bullet.travel(monsters, floor)
        if bullet.enabled == False: bullets.remove(bullet)

    if held_keys['left mouse'] and shot_time > 1:
        bullets.append(gun.Bullet(g))
        if shot_time > 1: shot_time = 0


    if shot_time < 2:
        relative_x, relative_y = g.screen_position.x, g.screen_position.y
        if mouse.x > relative_x:
            p.direction = "right"
        else:
            p.direction = "left"
        p.scale_y = 1.1
        p.scale_x = 1.4
        p.y -= .16
        p.x += 0.12
        p.texture = f"assets//animations//player//shoot//{p.direction}//{shot_time}"

    p_healthbar.value = p.health


app.run()
