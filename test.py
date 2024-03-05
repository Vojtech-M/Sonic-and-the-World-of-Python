import pyglet
from pyglet import shapes

window = pyglet.window.Window( fullscreen = False)

label = pyglet.text.Label('HELLO PYTHON !',
                          font_name='Times New Roman',
                          font_size=72,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center',
                         )
#image = pyglet.resource.image('papousek.jpeg')
circle = shapes.Circle(x = 100, y = 100, radius = 13, color=(2, 20, 200))

   # image.blit(0, 0)
@window.event
def on_key_press(symbol, modifiers):
    print("test")
    if symbol == pyglet.window.key.C: 
        print("Key C is pressed") 
       

@window.event
def on_mouse_motion(x, y, dx, dy):
    circle.x = x
    circle.y = y

batch = pyglet.graphics.Batch()

frames = []

for x in range(7):
    image = pyglet.image.load(
        "img/{x:02}.png".format(x = x )
    )
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    frames.append(
        pyglet.image.AnimationFrame(image, duration=0.1)        
    )

goblin_animation = pyglet.image.Animation(frames=frames)

goblin = pyglet.sprite.Sprite(
    img = goblin_animation,
    x=500,
    y=500,
    batch=batch
)

batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(0)
foreground = pyglet.graphics.Group(1)

health_bg = shapes.Rectangle(
    x =  400,
    y = 50,
    width = 800,
    height = 100,
    color = (80,69,69),
    batch = batch,
    group = background
)
health = shapes.Rectangle(
    x =  400,
    y =  50,
    width = 500,
    height = 100,
    color = (255,69,69),
    batch = batch,
    group = foreground
)



@window.event
def on_draw():
    window.clear()
    label.draw()
    circle.draw()
    batch.draw()
    goblin.draw()

#class Player():
    #phisical object


pyglet.app.run()


#window.set_fullscreen(False)
