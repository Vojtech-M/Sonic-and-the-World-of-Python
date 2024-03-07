import pyglet
from pyglet import shapes
from pyglet.window import key
from pyglet import clock
import math
import time
import calendar
import time

i = 0
def callback(dt):
    global i
    i += 1
    print(f"{str(i).zfill(2)} seconds since last callback")

label = pyglet.text.Label(i,
                          font_name='Times New Roman',
                          font_size=36,
                          x=200, y=200,
                          anchor_x='center', anchor_y='center',
                          )
        

clock.schedule_interval(callback, 1)

#def callback(dt):
   # print(f"{dt} seconds since last callback")

#clock.schedule_interval(callback, 2) 

<<<<<<< HEAD
=======
def timer(dt):
    print("test")
clock.schedule_interval(timer, 1) 



>>>>>>> c42e69552e4dcacd71d5bd9e71d5806df5a14667

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
        self.speed = 10
<<<<<<< HEAD
        self.square = shapes.Rectangle(x=200,y=0, width=200, height=200, color=(55,55,255),batch=self.batch)
    

=======
        
>>>>>>> c42e69552e4dcacd71d5bd9e71d5806df5a14667
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
        self.batch.draw()

<<<<<<< HEAD
    def update(self,dt: float) -> None:
        if self.directions['left']:
            self.circle.x -= self.speed + 2
=======


    def update(self,dt: float) -> None:
        if self.directions['left']:
            self.circle.x -= (self.speed + 2) * dt
>>>>>>> c42e69552e4dcacd71d5bd9e71d5806df5a14667

        if self.directions['right']:
            self.circle.x += self.speed + dt * 4
        if self.directions['up']:
            self.circle.y += self.speed + dt * 4
        if self.directions['down']:
            self.circle.y -= self.speed + dt * 4
        pass



#if __name__ == "__main__"
window = MyWindow(width=1280, height=720, caption="Sonic and the world of Python", resizable=True)
pyglet.clock.schedule_interval(window.update,1/60)
pyglet.app.run()

'''
#timer, not included in program
seconds=0
minutes =0

<<<<<<< HEAD
=======
#timer, not included in program
seconds=0
minutes =0

>>>>>>> c42e69552e4dcacd71d5bd9e71d5806df5a14667
while(1):
 
    print(f"{minutes}:{seconds}")
    time.sleep(1)
    seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1

<<<<<<< HEAD

=======
'''
>>>>>>> c42e69552e4dcacd71d5bd9e71d5806df5a14667
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def timer():
    seconds = 0
    while True:
        print(format_time(seconds), end='\r')
        time.sleep(1)
        seconds += 1

# Example usage:
timer()  # 
    '''