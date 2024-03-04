import pyglet

window = pyglet.window.Window( fullscreen = True)

label = pyglet.text.Label('HELLO PYTHON !',
                          font_name='Lilita One',
                          font_size=72,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center',
                         )
#image = pyglet.resource.image('papousek.jpeg')
@window.event
def on_draw():
    window.clear()

    label.draw()

   # image.blit(0, 0)


pyglet.app.run()


window.set_fullscreen(False)
