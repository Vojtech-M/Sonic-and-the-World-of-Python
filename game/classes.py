import pyglet
from pyglet import shapes
from pyglet.window import key
from pyglet import clock
import math
import time

pyglet.font.add_file('game/img/PublicPixel.ttf')
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
        self.set_location(x=400, y=200)
        self.set_minimum_size(width=400, height=400)
       
    
        
        #self.circle = shapes.Circle(x=640, y=360, radius=50, color=(250,50,30),batch=self.batch)
        self.ball_image = pyglet.image.load('game/img/00.png')
        self.circle = pyglet.sprite.Sprite(self.ball_image, x=50, y=50,batch=self.batch)
        
        self.label = pyglet.text.Label('Hello, world',
                                        font_name='Public Pixel',
                                        font_size=36,
                                        x=self.width//2, y=500,
                                        anchor_x='center', anchor_y='center',
                                        batch=self.batch)
        
        
        
        self.directions = {'left':False,'right':False,'up':False,'down':False}
        self.speed = 10

    def on_key_press(self,symbol: int,modifiers: int) -> None:
        if symbol == key.LEFT:
            self.directions['left'] = True
        if symbol == key.RIGHT:
            self.directions['right'] = True
        if symbol == key.UP:
            self.directions['up'] = True
        if symbol == key.DOWN:
            self.directions['down'] = True  

        if symbol == pyglet.window.key.C: 
            print("Key C is pressed")
            label.draw()
        pass

    def on_key_release(self,symbol: int,modifiers: int) -> None:
        if symbol == key.LEFT:
            self.directions['left'] = False
        if symbol == key.RIGHT:
            self.directions['right'] = False
        if symbol == key.UP:
            self.directions['up'] = False
        if symbol == key.DOWN:
            self.directions['down'] = False  
        pass


    def on_draw(self) -> None:
        self.clear()
        self.label.draw()
        self.timer.label.draw()
        self.batch.draw()
       

    def update(self,dt: float) -> None:
        self.timer.update(dt)
        if self.directions['left']:
            self.circle.x -= self.speed + 2

        if self.directions['right']:
            self.circle.x += self.speed + dt * 4
        if self.directions['up']:
            self.circle.y += self.speed + dt * 4
        if self.directions['down']:
            self.circle.y -= self.speed + dt * 4
        pass



#if __name__ == "__main__"
window = MyWindow(width=1280, height=720, caption="Sonic and the world of Python", resizable=True)
img = pyglet.image.load("game/img/logo.png")  # Correct the path if needed
window.set_icon(img)

pyglet.clock.schedule_interval(window.update,1/60)
pyglet.app.run()

