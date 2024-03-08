import pyglet
from pyglet.window import key

pyglet.font.add_file('img/PublicPixel.ttf')
PublicPixel = pyglet.font.load('Public Pixel')


class Timer:
    def __init__(self):
        self.elapsed_time = 0
        self.label = pyglet.text.Label('00:00',
                                        font_name='Public Pixel',
                                        font_size=36,
                                        x=300, y=300,
                                        anchor_x='center', anchor_y='center')

    def update(self, dt):
        self.elapsed_time += dt
        minutes = int(self.elapsed_time / 60)
        seconds = int(self.elapsed_time % 60)
        self.label.text = f'{minutes:02}:{seconds:02}'

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.timer = Timer()
        self.timer.label.x = self.width // 2
        self.timer.label.y = self.height - 50
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label('Hello, world',
                                        font_name='Times New Roman',
                                        font_size=36,
                                        x=300, y=300,
                                        anchor_x='center', anchor_y='center',
                                        batch=self.batch)
        
        self.directions = {'left':False,'right':False,'up':False,'down':False}
        self.speed = 10

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.directions['left'] = True
        if symbol == key.RIGHT:
            self.directions['right'] = True
        if symbol == key.UP:
            self.directions['up'] = True
        if symbol == key.DOWN:
            self.directions['down'] = True  

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.directions['left'] = False
        if symbol == key.RIGHT:
            self.directions['right'] = False
        if symbol == key.UP:
            self.directions['up'] = False
        if symbol == key.DOWN:
            self.directions['down'] = False  

    def on_draw(self):
        self.clear()
        self.timer.label.draw()
        self.batch.draw()

    def update(self, dt):
        self.timer.update(dt)
        if self.directions['left']:
            self.circle.x -= self.speed + 2
        if self.directions['right']:
            self.circle.x += self.speed + dt * 4
        if self.directions['up']:
            self.circle.y += self.speed + dt * 4
        if self.directions['down']:
            self.circle.y -= self.speed + dt * 4

window = MyWindow(width=1280, height=720, caption="Sonic and the world of Python", resizable=True)
pyglet.clock.schedule_interval(window.update,1/60)
pyglet.app.run()