import pyglet
from pyglet import shapes
from pyglet.window import key

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.set_location(x=400, y=200)
        self.set_minimum_size(width=400, height=400)

        self.batch = pyglet.graphics.Batch()
        #self.circle = shapes.Circle(x=640, y=360, radius=50, color=(250,50,30),batch=self.batch)
        self.ball_image = pyglet.image.load('img/00.png')
        self.circle = pyglet.sprite.Sprite(self.ball_image, x=50, y=50,batch=self.batch)
        self.directions = {'left':False,'right':False,'up':False,'down':False}
    def on_key_press(self,symbol: int,modifiers: int) -> None:
        if symbol == key.LEFT:
            self.directions['left'] = True
        if symbol == key.RIGHT:
            self.directions['right'] = True
        if symbol == key.UP:
            self.directions['up'] = True
        if symbol == key.DOWN:
            self.directions['down'] = True  
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
        self.batch.draw()

        pass
    def update(self,dt: float) -> None:
        if self.directions['left']:
            self.circle.x -= self.speed
        if self.directions['right']:
            self.circle.x += self.speed
        if self.directions['up']:
            self.circle.y += self.speed
        if self.directions['down']:
            self.circle.y -= self.speed
        pass

#if __name__ == "__main__"
window = MyWindow(width=1280, height=720, caption="Sonic and the world of Python", resizable=True)
pyglet.clock.schedule_interval(window.update,1/60)
pyglet.app.run()


