import pymunk
from cmu_112_graphics import *

class Ball(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.r = 10
        self.color = 'blue'
        self.body.position = cx, cy
        self.body = pymunk.Circle(1, 1000)
        self.shape = pymunk.Circle(body, r, (cx, cy))
        


def appStarted(app):
    app.balls = set()
    space = pymunk.Space()
    space.gravity = 0, -1000
    static_body = _space.static_body
    static_lines = [
        pymunk.Segment(static_body, (111.0, 600 - 280), (407.0, 600 - 246), 0.0),
        pymunk.Segment(static_body, (407.0, 600 - 246), (407.0, 600 - 343), 0.0),
    ]
    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.9

def mousePressed(app, event):
    app.balls.add(Ball(event.x, event.y))

def drawBalls(app, canvas):
    for ball in app.balls:
        cx = ball.cx 
        cy = ball.cy
        r = ball.r
        color = ball.color
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = color)

def redrawAll(app, canvas):
    drawBalls(app, canvas)

runApp(width = 600, height = 600)