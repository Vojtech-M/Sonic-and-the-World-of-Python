import pyglet
from pyglet import shapes
import sys

window = pyglet.window.Window( fullscreen = False)

label = pyglet.text.Label('HELLO PYTHONN !',
                          font_name='Times New Roman',
                          font_size=72,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center',
                         )
#image = pyglet.resource.image('papousek.jpeg')
circle = shapes.Circle(x = 100, y = 100, radius = 13, color=(255, 255, 255))

   # image.blit(0, 0)
@window.event
def on_key_press(symbol, modifiers):
    print("test")
    if symbol == pyglet.window.key.C: 
        print("Key C is pressed") 

def on_mouse_motion(x, y, dx, dy):
    circle.x = x
    circle.y = y
    
   
@window.event
def on_draw():
    window.clear()

    label.draw()
    circle.draw()



pyglet.app.run()


window.set_fullscreen(False)
